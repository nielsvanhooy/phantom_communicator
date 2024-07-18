import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks.helpers import get_match
from phantom_communicator.command_blocks.parsers.iosxe.show_version import parse_show_ver


@command_or_parse(name=commands.SHOW_SOFTWARE, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_software(command_results) -> dict[str, Any]:
    # i was expecting commands_results be a list here. need to find out.
    if command_results.cmd_type == "str":
        return parse_show_ver(command_results)

    if command_results.cmd_type == "snmp":
        loc_and_image = re.compile(r":(.*)")

        get_loc_image = get_match(
            command_results.result,
            loc_and_image,
        )

        return {"loc_and_image": get_loc_image}
