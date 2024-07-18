from phantom_communicator.command_blocks.command import Command
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name="show_startup_config", vendor="huawei", os="hvrp")
def show_startup_config() -> Command:
    return Command("display saved-configuration")
