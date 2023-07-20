import asyncio
import timeit
from pathlib import Path

import uvloop

from phantom_communicator.communicators.base import Communicator
from phantom_communicator.logger import logger


async def get_data(ip):
    communicator = Communicator.factory(host=ip, os="iosxe", username="test008", password="test008")

    async with communicator as conn:
        logger.warning(f"gathering info for {ip}")
        response = await conn.send_commands(
            [
                "copy run start\n",
                "show run",
                "show ip int brief",
            ]
        )
        version = await conn.get_version()
        startup_config = await conn.get_running_config()
        boot_files = await conn.get_boot_files()
        genie_output = await conn.genie_parse_output()

        response_two = await conn.send_interactive_command(
            [("copy run start", "Destination filename [startup-config]?", False), ("\n", "[OK]", False)]
        )

        get_running_config = await conn.save_device_config(ip)
        print(get_running_config, ip)


async def communicate():
    cpes = [
        # "10.1.1.154",
        # "10.17.28.193",
        # "10.1.1.155",
        # "10.17.28.194",
        "10.1.1.156",
    ]
    task_list = [asyncio.create_task(get_data(cpe)) for cpe in cpes]
    await asyncio.gather(*task_list)


if __name__ == "__main__":
    uvloop.install()
    file_path = Path("files/")
    if not file_path.is_dir():
        file_path.mkdir(parents=True, exist_ok=True)
    result = timeit.timeit("asyncio.run(communicate())", setup="from __main__ import communicate, asyncio", number=1)
    print(result)
