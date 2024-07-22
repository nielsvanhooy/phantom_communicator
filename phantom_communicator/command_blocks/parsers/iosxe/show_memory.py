import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks.helpers import get_match


@command_or_parse(name=commands.SHOW_MEMORY, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_memory(command_results) -> dict[str, Any]:

    data = command_results.result

    if command_results.command_name == "show memory statistics":
        processor_regex = re.compile(r"Processor\s+\w+\s+(\d+)\s+(\d+)\s+(\d+)")

        processor_memory_total = int(get_match(data, processor_regex))
        processor_memory_used = int(get_match(data, processor_regex, n=2))
        processor_memory_free = int(get_match(data, processor_regex, n=3))

        return {
            "total": processor_memory_total,
            "free": processor_memory_free,
            "used": processor_memory_used,
        }

    if command_results.command_name == "sh flash: | i bytes":
        flash_regex = re.compile(r"(.*) bytes available \((.*) bytes used")  # noqa

        flash_memory_free = int(get_match(data, flash_regex))
        flash_memory_used = int(get_match(data, flash_regex, n=2))

        return {
            "total": flash_memory_free + flash_memory_used if (flash_memory_free and flash_memory_used) else None,
            "free": flash_memory_free,
            "used": flash_memory_used,
        }
