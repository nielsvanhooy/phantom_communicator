# from scrapli import Scrapli
# from scrapli.driver.core import AsyncIOSXEDriver, IOSXEDriver
# from scrapli_cfg import AsyncScrapliCfg, ScrapliCfg
# from scrapli_cfg.platform.core.cisco_iosxe import ScrapliCfgIOSXE, AsyncScrapliCfgIOSXE
#
# from phantom_communicator.communicators.base import Communicator
# import asyncio
#
# # async def readout():
# #     communicator = Communicator.factory(host="10.1.1.152", username="lagen008", password="lagen008", os="iosxe")
# #     async with communicator as conn:
# #         await conn.send_commands(
# #             [
# #                 "copy run start\n",
# #                 "show run",
# #                 "show ip int brief",
# #             ],
# #         )
# #         await conn.get_version()
# #         await conn.get_startup_config()
# #         await conn.get_boot_files()
#
# #
# # asyncio.run(readout())
#
#
# # device = {
# #    "host": "10.1.1.152",
# #    "auth_username": "lagen008",
# #    "auth_password": "lagen008",
# #    "auth_strict_key": False,
# #    "platform": "cisco_iosxe",
# #    "ssh_config_file": "tests/config"
# # }
# #
# # conn = Scrapli(**device)
# # conn.open()
# # print(conn.get_prompt())
#
#
# from scrapli.driver.core import AsyncIOSXEDriver
# from scrapli_cfg.platform.core.cisco_iosxe import AsyncScrapliCfgIOSXE
#
# import asyncio
#
# import logging
# logging.basicConfig()
# lala = logging.getLogger().setLevel(logging.DEBUG)
#
#
# def test_sync():
#     device = {
#         "host": "10.1.1.156",
#         "auth_username": "lagen008",
#         "auth_password": "lagen008",
#         "auth_strict_key": False,
#         "ssh_config_file": "/Users/nielsvanhooij/git/new_bifrost_repos/phantom_communicator/phantom_communicator/config",
#     }
#
#     conn = IOSXEDriver(**device)
#     cfg_conn = ScrapliCfgIOSXE(conn=conn)
#     conn.open()
#     alive = conn.isalive()
#     cfg_conn.prepare()
#     version_result = cfg_conn.get_version()
#     print(version_result.result)
#
# test_sync()
#
# async def test():
#     device = {
#         "host": "10.1.1.156",
#         "auth_username": "lagen008",
#         "auth_password": "lagen008",
#         "auth_strict_key": False,
#         "transport": "asyncssh",
#         "ssh_config_file": "/Users/nielsvanhooij/git/new_bifrost_repos/phantom_communicator/phantom_communicator/config",
#     }
#     conn = AsyncIOSXEDriver(**device)
#     cfg_conn = AsyncScrapliCfgIOSXE(conn=conn, dedicated_connection=True)
#     await conn.open()
#     alive = conn.isalive()
#     await cfg_conn.prepare()
#     version_result = await cfg_conn.get_version()
#     print(version_result.result)
#
#     session = AsyncIOSXEDriver(**device)
#     await session.open()
#     alive_two = session.isalive()
#     cfg_conn = AsyncScrapliCfgIOSXE(conn=session)
#     await cfg_conn.prepare()
#     version_result = await cfg_conn.get_version()
#     print(version_result.result)
#
# asyncio.run(test())
