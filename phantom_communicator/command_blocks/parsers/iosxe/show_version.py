from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.command_result import CommandResult
from phantom_communicator.command_blocks.decorators import command_or_parse
import re

from phantom_communicator.command_blocks.helpers import get_match, generate_dict


@command_or_parse(name=commands.SHOW_VERSION, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_ver(command_results: CommandResult) -> dict[str, Any | None]:
    data = command_results.result

    bundle_rev = re.compile(r"\((.*)\), Version ([^,\s]*),")  # type: ignore[unreachable]
    bootloader_ios = re.compile(r"ootstrap,\s(.*),\s(.*)")
    bootloader_iosxe = re.compile(r"ROM: (.*)")

    get_bundle = get_match(data, bundle_rev)
    get_swrev = get_match(data, bundle_rev, n=2)

    bootloader_ios = get_match(data, bootloader_ios)
    bootloader_iosxe = get_match(data, bootloader_iosxe)
    bootloader = bootloader_ios or bootloader_iosxe or None

    return {
        "bootloaderrev": bootloader.rstrip() if bootloader else None,
        "bundle": get_bundle,
        "softwarerev": get_swrev,
    }
