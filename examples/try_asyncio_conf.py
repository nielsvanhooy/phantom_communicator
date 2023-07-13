import asyncio
import timeit

from phantom_communicator.communicator_asyncio import Communicator


async def get_data(ip):
    communicator = Communicator.factory(
        host=ip,
    )

    async with communicator as conn:
        response = await conn.send_command("conf t")
        response = await conn.send_command("int GigabitEthernet0/0/0")
        response = await conn.send_command("description this is a test")
        response = await conn.send_command("exit")
        # response_again = await conn.send_commands(["show run", 'show ip int brief', "show ip route"])
        print(f"gathered info for {ip}")


async def communicate():
    cpes = [
        "10.1.1.154",
    ]
    task_list = [asyncio.create_task(get_data(cpe)) for cpe in cpes]
    await asyncio.gather(*task_list)


if __name__ == "__main__":
    result = timeit.timeit("asyncio.run(communicate())", setup="from __main__ import communicate, asyncio", number=1)
    print(result)
