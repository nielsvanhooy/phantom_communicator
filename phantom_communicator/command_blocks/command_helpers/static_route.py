import re

from netaddr import IPAddress, IPNetwork, valid_ipv4, valid_ipv6

CISCO_PREFERENCE_STANDARD = 1
HUAWEI_HVRP_PREFERENCE_STANDARD = 60


def cisco_ipv4(static_route: str) -> dict:
    # Normalize interface names by removing extra spaces
    replace_patterns = {
        r"\bnull\b": "Null",
        r"\btunnel\b": "Tunnel",
        r"\bcellular\b": "Cellular",
    }
    for pattern, replacement in replace_patterns.items():
        static_route = re.sub(pattern, replacement, static_route, flags=re.IGNORECASE)

    # Handle special case for names with spaces
    if '"' in static_route:
        name_pattern = re.compile(r'(.*)"(.*)"(.*)')
        match = name_pattern.search(static_route)
        if match:
            static_route = f"{match.group(1)}{match.group(2).replace(' ', '_')}{match.group(3)}"

    # Split the route into components
    items = static_route.split()

    # Extract options based on predefined list
    option_list = [
        ("tag", 1),
        ("track", 1),
        ("vrf", 1),
        ("global", 0),
        ("permanent", 0),
        ("name", 1),
    ]
    static_route_dict = {}
    for option, offset in option_list:
        if option in items:
            index = items.index(option)
            # Adjust for boolean options that don't have a following value
            value = items[index + offset] if offset else True
            static_route_dict[option] = value
            # Remove the option and its value from items
            del items[index : index + 1 + offset]

    # Process IP address and subnet mask
    try:
        ip_address, subnet_mask, *items = items
        static_route_dict["ip_address"] = ip_address
        static_route_dict["ip_subnet_mask"] = subnet_mask
        static_route_dict["prefixlength"] = IPNetwork(f"{ip_address}/{subnet_mask}").prefixlen
        static_route_dict["version"] = IPAddress(ip_address).version
    except ValueError:
        raise ValueError("Invalid IP address or subnet mask provided.")

    # Determine if there's an interface or next hop IP
    if items:
        if "." in items[0] or ":" in items[0]:  # Next hop IP
            static_route_dict["next_hop"] = items.pop(0)
        else:  # Interface name
            static_route_dict["interface"] = items.pop(0)

    # Set preference if specified, else use default
    static_route_dict["preference"] = items.pop(0) if items and items[0].isdigit() else CISCO_PREFERENCE_STANDARD

    return static_route_dict


def cisco_ipv6(static_route: object) -> object:
    static_route_dict = {}
    items = static_route.split(" ")

    option_list = [
        ("tag", 1),
        ("track", 1),
        ("vrf", 1),
        ("name", 1),
        ("permanent", 0),
        ("global", 0),
    ]

    for option in option_list:
        value = None
        if option[0] in items:
            index = items.index(option[0])
            value = items[index + option[1]]
            del items[index : index + 1 + option[1]]
        static_route_dict[option[0]] = value

    ipv6address = IPNetwork(items[0])

    static_route_dict["ip_address"] = str(ipv6address.network)
    static_route_dict["ip_subnet_mask"] = ipv6address.prefixlen
    static_route_dict["prefixlength"] = ipv6address.prefixlen
    static_route_dict["version"] = ipv6address.version
    del items[0]

    static_route_dict["interface"] = None
    if items[0].count("::") != 1:
        static_route_dict["next_hop"] = items[1]
        static_route_dict["interface"] = items[0]
        del items[0:2]

    static_route_dict["preference"] = CISCO_PREFERENCE_STANDARD
    if len(items) != 0 and items[0].isdigit():
        static_route_dict["preference"] = items[0]
        del items[0]

    return static_route_dict


def huawei_ipv4v6(static_route: object) -> object:
    """
    ip route-static 192.168.28.0 255.255.255.0 NULL0 preference 250
    ip route-static x.x.x.x y.y.y.y <next-hop-IP> preference <z>
    ip route-static x.x.x.x y.y.y.y <next-hop-interface> preference <z>
    ip route-static x.x.x.x y.y.y.y <next-hop> preference <x>
                                    tag <tag> description <name>

    ipv6 route-static
    :return:
    """

    static_route_dict = {}

    option_list = [
        ("tag", "tag", 1),
        ("vpn-instance", "destinationvrf", 1),
        ("permanent", "permanent", 0),
        ("preference", "preference", 1),
        ("ldp-sync", "ldpsync", 0),
        ("dhcp", "dhcp", 0),
        ("inherit-cost", "inheritcost", 0),
    ]

    static_route = static_route.strip()

    items = static_route.split(" ")

    description = None
    track = None
    if "description" in items:
        position = items.index("description")
        description = " ".join(items[position + 1 :])
        del items[position::]

    if "track" in items:
        position = items.index("track")
        track = " ".join(items[position + 1 :])
        del items[position::]

    static_route_dict["name"] = description
    static_route_dict["track"] = track

    # because vpn-instance is allowed for source and destination we first
    # check if there is a source vrf
    # in option list we check for destination vrf
    # (this can be first instance or second)

    if items[0] == "vpn-instance":
        static_route_dict["vrf"] = items[1]
        del items[0:2]

    for option in option_list:
        value = None
        if option[0] in items:
            index = items.index(option[0])
            value = items[index + option[2]]
            del items[index : index + 1 + option[2]]
        static_route_dict[option[1]] = value

    static_route_dict["ip_address"] = items[0]
    static_route_dict["ip_subnet_mask"] = items[1]
    try:
        static_route_dict["prefixlength"] = IPNetwork(f"{items[0]}/" f"{items[1]}").prefixlen
    except IndexError as e:
        msg = f"Error Extract static-route {e} static_route"
        raise IndexError(msg)

    static_route_dict["version"] = IPAddress(items[0]).version
    del items[0:2]

    static_route_dict["interface"] = None

    # has interface as next hop interface
    # test ipv4 and ipv6 . or :
    if items and (items[0].count(".") != 3 or items[0].count(":") == 0):
        static_route_dict["interface"] = items[0]

        del items[0]
    # has ip as next hop
    if items and (items[0].count(".") == 3 or items[0].count(":") != 0):
        static_route_dict["next_hop"] = items[0]
        del items[0]

    if not static_route_dict["preference"]:
        static_route_dict["preference"] = HUAWEI_HVRP_PREFERENCE_STANDARD

    return static_route_dict


def is_valid_ip(static_route: object) -> bool:
    offset = 0
    static_route = static_route.strip()
    items = static_route.split(" ")
    if items[0] == "vrf" or items[0] == "vpn-instance":
        offset = 2

    return True if (valid_ipv4(items[offset], flags=1) or valid_ipv6(items[offset].split("/")[0])) else False
