import pytest
from scrapli.driver.core import AsyncIOSXEDriver, IOSXEDriver

from phantom_communicator.communicator_asyncio import Communicator

# 10.1.1.131


@pytest.mark.scrapli_replay
async def test_vrp_communicator():
    communicator = Communicator.factory(host="10.1.1.131", os="vrp")
    async with communicator as conn:
        response = await conn.send_command("display current-configuration")
        version = await conn.get_version()
        lala = await conn.get_startup_config()
        boot_files = await conn.get_boot_files()
        get_running_config = await conn.save_device_config("10.1.1.131")
