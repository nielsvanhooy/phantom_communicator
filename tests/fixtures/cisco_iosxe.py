import pytest

from phantom_communicator.command_blocks.command_block import CommandBlock


@pytest.fixture
def cb_cisco():
    return CommandBlock.factory(vendor="cisco", os="iosxe")


