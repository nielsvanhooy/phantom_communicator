from phantom_communicator.command_blocks.command import Command, SNMPCommand
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks import constants as commands


@command_or_parse(name=commands.SHOW_SOFTWARE, vendor=commands.CISCO, os="iosxe")
def show_software(*args, **kwargs) -> list:
    return [Command("show ver"), SNMPCommand("1.3.6.1.4.1.9.2.1.73.0")]
