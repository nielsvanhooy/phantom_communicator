from phantom_communicator.command_blocks.command import Command
from phantom_communicator.command_blocks.decorators import command
from phantom_communicator.command_blocks.snmp_command import SNMPCommand


@command(name="show_version", vendor="cisco", os="iosxe")
def show_ver(*args, **kwargs) -> Command:
    return Command("show ver")


@command(name="setup_session", vendor="cisco", os="iosxe")
def setup_session() -> Command:
    return Command("terminal length 0")


@command(name="show_software", vendor="cisco", os="iosxe")
def show_software(*args, **kwargs) -> list:
    return [Command("show ver"), SNMPCommand(".1.3.6.1.4.1.9.2.1.73.0")]