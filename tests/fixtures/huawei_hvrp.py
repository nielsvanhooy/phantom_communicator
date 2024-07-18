import pytest

from phantom_communicator.command_blocks.command_and_parse import CommandParser


@pytest.fixture
def cb_huawei():
    return CommandParser.factory(vendor="huawei", os="hvrp")
