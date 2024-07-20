import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks.helpers import convert_to_epoch


@command_or_parse(name=commands.SHOW_UPTIME, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_uptime(command_results) -> dict[str, Any]:
    data = command_results.result

    uptime_regex = re.compile(r".*uptime is (.*)")
    uptime = re.findall(uptime_regex, data)
    components = uptime[0].split(", ")
    units_singular = {
        "year": "years",
        "week": "weeks",
        "day": "days",
        "hour": "hours",
        "minute": "minutes",
        "second": "seconds",
    }

    uptime_dict = {}
    for component in components:
        value, unit = component.split(maxsplit=1)
        unit_singular = units_singular.get(unit.rstrip("s"), unit)
        uptime_dict[unit_singular] = int(value)

    uptime_dict["epoch"] = convert_to_epoch(uptime_dict)

    return uptime_dict
