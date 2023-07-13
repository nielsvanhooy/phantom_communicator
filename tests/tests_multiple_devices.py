import asyncio
import time

import uvloop

from phantom_communicator.communicator_asyncio import Communicator

devices = [
    ("10.1.1.151", "iosxe"),
    ("10.1.1.142", "ios"),
    ("10.1.1.138", "vrp"),
    ("10.1.1.130", "vrp"),
    ("10.1.1.132", "vrp"),
    ("10.1.1.248", "vrp"),
    ("10.1.1.131", "vrp"),
    ("10.1.1.154", "iosxe"),
    # ("10.17.28.191" , "iosxr"),
    ("10.17.28.193", "iosxe"),
    ("10.1.1.155", "iosxe"),
    ("10.1.1.156", "iosxe"),
    ("10.17.28.194", "iosxe"),
    # ("10.17.28.195", "iosxr"),
    ("10.1.1.153", "ios"),
]


async def communicate_with_devices(devices):
    start = time.time()
    tasks = [asyncio.create_task(communicate(host, os)) for host, os in devices]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    end = time.time()
    print(end - start)
    return results


async def communicate(host, os):
    communicator = Communicator.factory(host=host, os=os)

    data = [host, os]
    async with communicator as conn:
        version = await conn.get_version()
        startup_config = await conn.get_startup_config()
        data.extend((version, startup_config))
    return data


if __name__ == "__main__":
    uvloop.install()
    asyncio.run(communicate_with_devices(devices))
