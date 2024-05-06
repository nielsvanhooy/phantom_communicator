import re
from collections import namedtuple

from scrapli.driver.core import AsyncIOSXEDriver
from scrapli_cfg import AsyncScrapliCfg

from phantom_communicator.command_blocks.command_block import CommandBlock
from phantom_communicator.communicators.base import BaseCommunicator
from phantom_communicator.constants import CONFIGSTORE, GET_BOOT_STATEMENTS_IOSXE

BootFiles = namedtuple("BootFiles", ["main", "backup"])


class CiscoIosXeCommunicator(BaseCommunicator):
    def __init__(self, host, username, password, os):
        super().__init__(host, username, password, os)
        self._session = AsyncIOSXEDriver(
            host=self.host,
            auth_username=self.username,
            auth_password=self.password,
            auth_strict_key=False,
            transport="asyncssh",
            ssh_config_file="config",
        )
        self._cfg_conn = AsyncScrapliCfg(self._session, dedicated_connection=True)
        self.command_block = CommandBlock.factory(vendor="cisco", os=self.os)

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
            overwrite=True,
            force_config=True,
            cleanup=False,
        )
