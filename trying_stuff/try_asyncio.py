import timeit

import uvloop

from communicator_asyncio import Communicator
import asyncio


async def get_data(ip):
    communicator = Communicator.factory(host=ip, os="iosxe")

    async with communicator as conn:
        # response_again = await conn.send_commands(["show run", 'show ip int brief', "show ip route"])
        print(f"gathered info for {ip}")
        response = await conn.send_commands([
            "show ip route",
            "show run",
            "show ip int brief"
            "wr mem"
            "copy run start"
        ])
        version = await conn.get_version()
        startup_config = await conn.get_startup_config()
        boot_files = await conn.get_boot_files()

        get_running_config = await conn.save_device_config(ip)
        print(get_running_config, ip)


async def communicate():
    cpes = [
        # "10.1.1.154",
        "10.17.28.193",
        # "10.1.1.155",
        "10.17.28.194",
        # "10.1.1.156",
    ]
    task_list = [asyncio.create_task(get_data(cpe)) for cpe in cpes]
    await asyncio.gather(*task_list)


if __name__ == "__main__":
    uvloop.install()
    result = timeit.timeit("asyncio.run(communicate())", setup="from __main__ import communicate, asyncio", number=1)
    print(result)
