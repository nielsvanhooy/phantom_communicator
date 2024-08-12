from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_FEATURESET, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_featureset(command_results) -> dict[str, Any]:
    data = command_results.result
    return {"featureset": data.replace('"', "")}
