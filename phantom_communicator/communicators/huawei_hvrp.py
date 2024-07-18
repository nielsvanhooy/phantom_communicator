import re
from collections import namedtuple

from scrapli_cfg import AsyncScrapliCfg
from scrapli_community.huawei.vrp.async_driver import (
    AsyncHuaweiVRPDriver,
    default_async_on_close,
    default_async_on_open,
)
from scrapli_community.huawei.vrp.huawei_vrp import DEFAULT_PRIVILEGE_LEVELS as VRP_DEFAULT_PRIVILEGE_LEVELS

from phantom_communicator.command_blocks.command_and_parse import CommandParser
from phantom_communicator.communicators.base import BaseCommunicator
from phantom_communicator.constants import CONFIGSTORE, GET_BOOT_STATEMENTS_HVRP

BootFiles = namedtuple("BootFiles", ["main", "backup"])


class HuaweiVrpCommunicator(BaseCommunicator):
    def __init__(self, host, username, password, os):
        super().__init__(host, username, password, os)
        self._session = AsyncHuaweiVRPDriver(
            host=self.host,
            auth_username=self.username,
            auth_password=self.password,
            auth_strict_key=False,
            transport="asyncssh",
            ssh_config_file="../config",
            privilege_levels=VRP_DEFAULT_PRIVILEGE_LEVELS,
            default_desired_privilege_level="privilege_exec",
            on_open=default_async_on_open,
            on_close=default_async_on_close,
        )
        self._cfg_conn = AsyncScrapliCfg(self._session)
        self.command_block = CommandParser.factory(vendor="huawei", os=self.os)

    def __repr__(self) -> str:
        return f"HuaweiVrpCommunicator({self.host=}"

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
        get_boot_config_statement = await self._session.send_command("display startup")

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
