import re

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.command_helpers.static_route import cisco_ipv4, cisco_ipv6, is_valid_ip
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_RUN_IP_ROUTE, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_run_ip_route(command_results) -> list[object] | None:
    data = command_results.result

    regex_block = re.compile(r"^(ip|ipv6)\sroute\s(.*)\n", re.MULTILINE)
    static_routes = []

    for match in regex_block.finditer(data):
        protocol, route = match.groups()
        if not is_valid_ip(route):
            continue
        try:
            route_info = cisco_ipv6(route) if protocol == "ipv6" else cisco_ipv4(route)
            route_info["preference"] = int(route_info.get("preference", 0)) or None
            route_info["tag"] = int(route_info.get("tag") if route_info.get("tag") is not None else 0) or None
            route_info["permanent"] = route_info.get("permanent", "") == "permanent"
            route_info["global"] = route_info.get("global", "") == "global"
            route_info["ip_subnet"] = route_info.pop("ip_address", None)
            static_routes.append(route_info)
        except IndexError:
            # if input values are incorrect or empty
            continue

    return static_routes if static_routes else None
