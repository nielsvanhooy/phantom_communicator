import pytest

from phantom_communicator.command_blocks.command_block import CommandBlock


@pytest.fixture
def cb_huawei():
    return CommandBlock.factory(vendor="huawei", os="hvrp")
