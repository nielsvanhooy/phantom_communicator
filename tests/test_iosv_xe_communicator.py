import pytest

from phantom_communicator.communicator_asyncio import Communicator
from scrapli_transfer_utils import AsyncSrapliTransferUtils

@pytest.mark.asyncio
async def test_iosv_xe_communicator():
    communicator = Communicator.factory(host="10.1.1.156", os="iosxe")
    async with communicator as conn:
        response = await conn.send_command("show ip int brief")
        version = await conn.get_version()
        startup_config = await conn.get_startup_config()
        boot_files = await conn.get_boot_files()

        get_running_config = await conn.file_transfer(
            operation='get',
            src="running-config",
            dst="files/test",
            verify=True,
            force_config=True,
            device_fs="system:"
        )
        lala = "loeloe"
