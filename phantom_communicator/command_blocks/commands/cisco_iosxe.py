from phantom_communicator.command_blocks.command import Command
from phantom_communicator.command_blocks.decorators import command


@command(name="show_version", vendor="cisco", os="iosxe")
def show_ver(*args, **kwargs) -> Command:
    return Command("show ver")


@command(name="setup_session", vendor="cisco", os="iosxe")
def setup_session() -> Command:
    return Command("terminal length 0")
