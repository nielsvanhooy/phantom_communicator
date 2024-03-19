import pytest

from phantom_communicator.communicators.base import Communicator
from phantom_communicator.communicators.cisco_iosxe import CiscoIosXeCommunicator

from phantom_communicator.exceptions import CommunicatorAuthenticationFailed
from tests.fake_cfg_conn import FakeCfgConn


# @pytest.mark.scrapli_replay
# async def __test_iosv_xe_communicator(monkeypatch):
#     communicator = Communicator.factory(host="10.1.1.156", os="iosxe")
#     communicator._cfg_conn = FakeCfgConn()
#     async with communicator as conn:
#         response = await conn.send_command("show ip int brief")
#         version = await conn.get_version()
#         startup_config = await conn.get_startup_config()
#         boot_files = await conn.get_boot_files()
#
#         get_running_config = await conn.file_transfer(
#             operation="get", src="running-config", dst="../files/test", verify=True, force_config=True, device_fs="system:"
#         )
#         lala = "loeloe"


async def test_iosv_xe_communicator_selected(iosxe_communicator):
    assert iosxe_communicator.os == "iosxe"
    assert isinstance(iosxe_communicator, CiscoIosXeCommunicator)


@pytest.mark.scrapli_replay
async def test_iosv_xe_communicator_send_command(iosxe_communicator):
    expected_result = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0/0   192.168.12.17   YES NVRAM  up                    up
GigabitEthernet0/0/1   unassigned      YES NVRAM  up                    up
GigabitEthernet0/0/2   unassigned      YES NVRAM  down                  down
Cellular0/1/0          10.124.234.45   YES IPCP   up                    up
Cellular0/1/1          unassigned      YES NVRAM  administratively down down
GigabitEthernet0       unassigned      YES unset  administratively down down
Loopback0              10.1.1.156      YES NVRAM  up                    up
Tunnel10               10.1.1.242      YES NVRAM  up                    down"""

    cmd = "show ip int brief"

    async with iosxe_communicator as conn:
        response = await conn.send_command(cmd)

    assert response.result == expected_result
    assert response.channel_input == cmd

    assert iosxe_communicator.channel_io[0]["command_input"] == cmd
    assert iosxe_communicator.channel_io[0]["command_output"] == expected_result


@pytest.mark.scrapli_replay
async def test_iosv_xe_communicator_send_commands(iosxe_communicator):
    expected_result = [
        """GigabitEthernet0/0/0   192.168.12.17   YES NVRAM  up                    up
GigabitEthernet0/0/1   unassigned      YES NVRAM  up                    up
GigabitEthernet0/0/2   unassigned      YES NVRAM  down                  down
GigabitEthernet0       unassigned      YES unset  administratively down down""",
        "Cisco IOS XE Software, Version 16.09.07",
    ]

    cmds = ["show ip int brief | i GigabitEthernet0", "show version | i Cisco IOS XE Software"]

    async with iosxe_communicator as conn:
        response = await conn.send_commands(cmds)

    for data in response.data:
        assert data.result in expected_result

    for cmd in conn.channel_io:
        assert cmd["command_input"] in cmds

    for cmd in conn.channel_io:
        assert cmd["command_output"] in expected_result


# # @pytest.mark.scrapli_replay
# async def test_iosv_xe_communicator_parse_genie(iosxe_communicator, caplog):
#
#     cmds = ["show version", "show ip route", "show run", "show ip route static", "show running-config | i ^ip route"]
#
#     async with iosxe_communicator as conn:
#         response = await conn.send_commands(cmds)
#         genie_output = await conn.genie_parse_output()
#
#     print(genie_output['show ip route static'])
#     lala = "loeloe"

async def test_iosv_xe_communicator_cant_connect():
    with pytest.raises(CommunicatorAuthenticationFailed):
        communicator = Communicator.factory(
            host="10.1.1.200", username="test008", password="test008", os="iosxe"
        )
        communicator._cfg_conn = FakeCfgConn()
        async with communicator as conn:
            conn.get_version()


async def test_iosv_xe_communicator_auth_failed():
    with pytest.raises(CommunicatorAuthenticationFailed):
        communicator = Communicator.factory(
            host="10.1.1.156", username="test008", password="test008", os="iosxe"
        )
        communicator._cfg_conn = FakeCfgConn()
        async with communicator as conn:
            conn.get_version()

### test _cfg_conn calling against he fake mock


@pytest.mark.scrapli_replay
async def test_iosv_xe_communicator_fake_cfgconn(iosxe_communicator):
    """this just tests the functionality of being called
    not the direct implemenation. that is tested in its own library
    """
    async with iosxe_communicator as conn:
        version = await conn.get_version()
        startup_config = await conn.get_startup_config()
        running_config = await conn.get_running_config()

    assert version == "i am a fake version"
    assert startup_config == "fake config"
    assert running_config == "fake config"
