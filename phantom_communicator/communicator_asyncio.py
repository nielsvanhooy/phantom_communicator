import asyncio
import re

from collections import namedtuple
from typing import Optional, Literal

from asyncssh import ConnectionLost
from scrapli.driver.core import AsyncIOSXEDriver
from scrapli.exceptions import ScrapliAuthenticationFailed
from scrapli_cfg import AsyncScrapliCfg
from scrapli_community.huawei.vrp.async_driver import (
    AsyncHuaweiVRPDriver,
    default_async_on_open,
    default_async_on_close,
)
from scrapli_community.huawei.vrp.huawei_vrp import DEFAULT_PRIVILEGE_LEVELS as VRP_DEFAULT_PRIVILEGE_LEVELS
from scrapli_transfer_utils import AsyncSrapliTransferUtils

from constants import GET_BOOT_STATEMENTS_IOSXE, GET_BOOT_STATEMENTS_HVRP, TACACS_WRITE_USER_NAME, \
    TACACS_WRITE_USER_PASS, CONFIGSTORE
from exceptions import CommunicatorNotFound, CommunicatorAuthenticationFailed

BootFiles = namedtuple("BootFiles", ["main", "backup"])


class Communicator:
    def __init__(
            self,
            host,
            username,
            password,
            os,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.os = os
        self.session = None
        self.cfg_conn = None

    @classmethod
    def factory(
            cls,
            host=None,
            username=TACACS_WRITE_USER_NAME,
            password=TACACS_WRITE_USER_PASS,
            os=None,
    ):
        return BaseCommunicator.factory(
            host=host,
            username=username,
            password=password,
            os=os,
        )

    async def send_command(self, command: str):
        raise NotImplemented

    async def send_commands(self, commands: list):
        raise NotImplemented

    async def get_version(self):
        version_result = await self.cfg_conn.get_version()
        return version_result.result

    async def get_startup_config(self):
        startup_config_result = await self.cfg_conn.get_config(source="startup")
        return startup_config_result.result

    async def get_running_config(self):
        running_config_result = await self.cfg_conn.get_config(source="running")
        return running_config_result.result

    async def get_boot_files(self):
        raise NotImplemented

    async def save_device_config(self, hostname: str):
        raise NotImplemented

    async def file_transfer(self,
                            operation: Literal["get", "put"],
                            src: str,
                            dst: str = "",
                            verify: bool = True,
                            device_fs: Optional[str] = None,
                            overwrite: bool = False,
                            force_config: bool = False,
                            cleanup: bool = True):
        """
        :param operation: put/get file to/from device
        :param src: source file name
        :param dst: destination file name (same as src if omitted)
        :param verify: `True` if verification is needed (checksum, file existence, disk space)
        :param device_fs: (autodetect if empty) is not always correct in guessing tho
        :param force_config: If set to `True`, Transfer function will be enabled in device configuration
                               before transfer.
                              If set to `False`, Transfer functionality will be checked but won't
                              configure the device.
                              If set to `None`, capability won't even checked.
        :param overwrite: If set to `True`, destination will be overwritten in case hash verification
                          fails
                          If set to `False`, destination file won't be overwritten.
                          Beware: turning off `verify` will make this parameter ignored and destination
                          will be overwritten regardless! (Logic is that if user does not care about
                          checking, just copy it over)
        :param cleanup: If set to True, call the cleanup procedure to restore configuration if it was
                     altered
        :return: example: FileTransferResult(exists=True, transferred=True, verified=True)
        """
        scp = AsyncSrapliTransferUtils(self.session)
        return await scp.file_transfer(
            operation=operation,
            src=src,
            dst=dst,
            verify=verify,
            device_fs=device_fs,
            force_config=force_config,
            cleanup=cleanup,
            overwrite=overwrite
        )

    async def __aenter__(self):
        retry = 0
        connection = False
        while not connection:
            try:
                await self.session.open()
                if self.cfg_conn:
                    await self.cfg_conn.prepare()
                connection = True

            except (ConnectionRefusedError, ConnectionLost) as e:
                retry += 1
                if retry > 10:
                    raise ConnectionLost("lost connection") from e
                await asyncio.sleep(1)

            except ScrapliAuthenticationFailed as e:
                raise CommunicatorAuthenticationFailed(
                    f"Failed to connect to {self.host} with os: {self.os} reason: {e}"
                ) from e

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


class BaseCommunicator(Communicator):
    @classmethod
    def factory(cls, *args, **kwargs):
        if kwargs.get("os") == "vrp":
            return HuaweiVrpCommunicator(*args, **kwargs)
        elif kwargs.get("os") in ["ios", "iosxe"]:
            return CiscoIosXeCommunicator(*args, **kwargs)
        raise CommunicatorNotFound(f"No Communicator defined for {kwargs.get('os')}")

    def __init__(self, host, username, password, os):
        super().__init__(host, username, password, os)

    async def send_command(self, command: str):
        return await self.session.send_command(command)

    async def send_commands(self, commands: list):
        return await self.session.send_commands(commands)


class CiscoIosXeCommunicator(BaseCommunicator):
    def __init__(self, host, username, password, os):
        super().__init__(host, username, password, os)
        self.session = AsyncIOSXEDriver(
            host=self.host,
            auth_username=self.username,
            auth_password=self.password,
            auth_strict_key=False,
            transport="asyncssh",
            ssh_config_file="config",
        )
        self.cfg_conn = AsyncScrapliCfg(self.session)

    async def get_boot_files(self) -> BootFiles:
        boot_files = await self.send_command(GET_BOOT_STATEMENTS_IOSXE)

        """
        boot-start-marker
        boot system flash:c800-universalk9-mz.SPA.154-3.M7.bin
        boot system flash:c800-universalk9-mz.SPA.154-3.M2.bin
        boot-end-marker
        """

        results = re.findall(r"boot system (?:flash|bootflash):(.*?)$", boot_files.result, re.MULTILINE)
        main = results[0] if results else None
        backup = results[1] if len(results) >= 2 else None

        return BootFiles(main, backup)

    async def save_device_config(self, hostname):
        return await self.file_transfer(
            operation="get",
            src="running-config",
            dst=f"{CONFIGSTORE}/{hostname}",
            verify=True,
            device_fs="system:",
            overwrite=False,
            force_config=True,
            cleanup=False,
        )


class HuaweiVrpCommunicator(BaseCommunicator):
    def __init__(self, host, username, password, os):
        super().__init__(host, username, password, os)
        self.session = AsyncHuaweiVRPDriver(
            host=self.host,
            auth_username=self.username,
            auth_password=self.password,
            auth_strict_key=False,
            transport="asyncssh",
            ssh_config_file="config",
            privilege_levels=VRP_DEFAULT_PRIVILEGE_LEVELS,
            default_desired_privilege_level="privilege_exec",
            on_open=default_async_on_open,
            on_close=default_async_on_close,
        )
        self.cfg_conn = AsyncScrapliCfg(self.session)

    async def get_boot_files(self):
        """
        Example command output:

        MainBoard:
          Startup system software:                   flash:/AR657W-V300R019C10SPC200.cc
          Next startup system software:              flash:/AR657W-V300R019C10SPC200.cc
          Backup system software for next startup:   null
          Startup saved-configuration file:          flash:/21500104862SL2600489-1595393893790.cfg
          Next startup saved-configuration file:     flash:/21500104862SL2600489-1595393893790.cfg
          Startup license file:                      null
          Next startup license file:                 null
          Startup patch package:                     null
          Next startup patch package:                null
          Startup voice-files:                       null
          Next startup voice-files:                  null

        :return:
        """
        boot_files = await self.send_command(GET_BOOT_STATEMENTS_HVRP)

        main = re.search(r"Startup system software:\s+flash:/(.*?)$", boot_files.result, re.MULTILINE)
        main = main[1] if main else None

        # backup = re.search(
        #     r"Backup system software for next startup:\s+(.*?)$",
        #     boot_files, re.MULTILINE)
        # backup = backup[1] if backup else None

        """
        We are not utilising the huawei backup feature as this is not quite 
        what we'd expect. 

        As discussed on 22-07-2020; we won't be setting the backup image for huawei.
        The inner workings are as follows:

        - Set "next" startup system-software
        - This will make it so that on next boot it will try to boot that image
        - If boot fails 3 times, it will go back to "current" which is the working
        image that still works
        - Backup would only be necessary in the case that doesn't work, but it's
        very unlikely as:
            A) even in a test scenario this was not possible to reproduce
            B) the "current" would also not be able to boot
        - Another note is there is not enough space for 3 image files on almost all huawei's.
        """

        return BootFiles(main=main, backup=None)

    async def save_device_config(self, hostname):
        get_boot_config_statement = await self.session.send_command("display startup")

        pattern = "Startup saved-configuration file: * flash:/(.*)"
        src_path = re.search(pattern, get_boot_config_statement.result)

        return await self.file_transfer(
            operation="get",
            src=src_path[1],
            dst=f"{CONFIGSTORE}/{hostname}",
            verify=True,
            overwrite=True,
            force_config=True,
            cleanup=False,
        )
