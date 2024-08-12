import pytest

from phantom_communicator.communicators.base import Communicator
from phantom_communicator.communicators.huawei_hvrp import HuaweiVrpCommunicator
from tests.fake_cfg_conn import FakeCfgConn

# 10.1.1.131


# @pytest.mark.scrapli_replay
# async def test_vrp_communicator():
#     communicator = Communicator.factory(host="10.1.1.131", os="vrp")
#     communicator._cfg_conn = FakeCfgConn()
#     async with communicator as conn:
#         response = await conn.send_command("display interfaces")
#         version = await conn.get_version()
#         lala = await conn.get_startup_config()
#         boot_files = await conn.get_boot_files()
#         get_running_config = await conn.save_device_config("10.1.1.131")


async def test_vrp_communicator_selected(vrp_communicator):
    assert vrp_communicator.os == "vrp"
    assert isinstance(vrp_communicator, HuaweiVrpCommunicator)


@pytest.mark.scrapli_replay
async def test_vrp_communicator_send_command(vrp_communicator):
    expected_result = """PHY: Physical
*down: administratively down
(l): loopback
 (s): spoofing
(b): BFD down
^down: standby
(e): ETHOAM down
(v): VirtualPort
 InUti/OutUti: input utility/output utility
Interface                   PHY   Protocol  InUti OutUti   inErrors  outErrors
Cellular0/0/0               up    up        0.01%  0.01%          0          0
GigabitEthernet0/0/0        *down down         0%     0%          0          0
GigabitEthernet0/0/1        *down down         0%     0%          0          0
GigabitEthernet0/0/2        *down down         0%     0%          0          0
GigabitEthernet0/0/3        *down down         0%     0%          0          0
GigabitEthernet0/0/4        *down down         0%     0%          0          0
GigabitEthernet0/0/5        *down down         0%     0%          0          0
GigabitEthernet0/0/6        *down down         0%     0%          0          0
GigabitEthernet0/0/7        *down down         0%     0%          0          0
GigabitEthernet0/0/8        up    up        0.01%  0.01%          0          0
GigabitEthernet0/0/9        down  down         0%     0%          0          0
GigabitEthernet0/0/10(v)    up    down         0%     0%          0          0
LoopBack0                   up    up(s)        --     --          0          0
NULL0                       up    up(s)        --     --          0          0
Tunnel0/0/10                up    up           --     --          0          0
Vlanif1                     *down down         --     --          0          0"""

    cmd = "display interface brief"

    async with vrp_communicator as conn:
        response = await conn.send_command(cmd)

    assert response.result == expected_result
    assert response.command_name == cmd

    assert vrp_communicator.channel_io[cmd]["result"] == expected_result


@pytest.mark.scrapli_replay
async def test_vrp_communicator_send_commands(vrp_communicator):
    expected_result = [
        "Description:HUAWEI, AR Series, GigabitEthernet0/0/0 Interface",
        "Description:HUAWEI, AR Series, GigabitEthernet0/0/1 Interface",
    ]

    cmds = [
        "display interface GigabitEthernet 0/0/0 | include Description",
        "display interface GigabitEthernet 0/0/1 | include Description",
    ]

    async with vrp_communicator as conn:
        response = await conn.send_commands(cmds)

    for data in response.data:
        assert data.result in expected_result

    for cmd in conn.channel_io:
        assert cmd["command_input"] in cmds

    for cmd in conn.channel_io:
        assert cmd["command_output"] in expected_result


@pytest.mark.scrapli_replay
async def test_vrp_communicator_get_version(vrp_communicator):
    """this just tests the functionality of being called
    not the direct implemenation. that is tested in its own library
    """
    async with vrp_communicator as conn:
        version = await conn.get_version()
        startup_config = await conn.get_startup_config()
        running_config = await conn.get_running_config()

    assert version == "i am a fake version"
    assert startup_config == "fake config"
    assert running_config == "fake config"
