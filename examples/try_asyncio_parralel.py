import asyncio
import concurrent.futures
import timeit
from multiprocessing import cpu_count

from phantom_communicator.communicator_asyncio import Communicator

NUM_CORES = cpu_count()


def process_starter():
    cpes = [
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
        "10.1.1.154",
        "10.17.28.193",
        "10.1.1.155",
        "10.17.28.194",
        "10.1.1.156",
    ]
    asyncio.run(loeloe(cpes))


async def loeloe(cpes):
    task_list = [asyncio.create_task(get_data(cpe)) for cpe in cpes]
    await asyncio.gather(*task_list)


async def get_data(ip):
    communicator = Communicator.factory(
        host=ip,
    )

    async with communicator as conn:
        response = await conn.send_command("show ip route")
        response = await conn.send_command("show run")
        response = await conn.send_command("show ip int brief")
        # response_again = await conn.send_commands(["show run", 'show ip int brief', "show ip route"])
        print(f"gathered info for {ip}")


def communicate():
    futures = []
    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        for _ in range(4):
            new_future = executor.submit(process_starter)
            futures.append(new_future)
    print(futures)
    concurrent.futures.wait(futures)


if __name__ == "__main__":
    print(NUM_CORES)
    result = timeit.timeit("communicate()", setup="from __main__ import communicate, asyncio", number=1)
    print(result)
