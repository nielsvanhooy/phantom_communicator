import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks.helpers import get_match


@command_or_parse(name=commands.SHOW_FLASH_STATISTICS, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_flash_statistics(command_results) -> dict[str, Any]:
    data = command_results.result

    flash_regex = re.compile(r"(.*) bytes available \((.*) bytes used")  # noqa

    flash_memory_free = int(get_match(data, flash_regex))
    flash_memory_used = int(get_match(data, flash_regex, n=2))

    return {
        "total": flash_memory_free + flash_memory_used if (flash_memory_free and flash_memory_used) else None,
        "free": flash_memory_free,
        "used": flash_memory_used,
    }
