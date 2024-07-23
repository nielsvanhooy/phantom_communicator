from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.command_helpers.get_config_item import get_config_item
from phantom_communicator.command_blocks.command_helpers.get_config_value import get_config_value
from phantom_communicator.command_blocks.command_helpers.get_config_value_position import get_config_value_position
from phantom_communicator.command_blocks.decorators import command_or_parse


def transform_domain_name(hostconf: dict[str, Any]) -> None:
    hostconf["domain_name"] = "".join(map(str, hostconf["domain_name"])) or None


def transform_pin(hostconf: dict[str, Any]) -> None:
    hostconf["pin"] = any(hostconf.get(key) for key in ["pin", "pin_1", "pin_2"])
    for key in ["pin_1", "pin_2"]:
        del hostconf[key]


def transform_snmp(hostconf: dict[str, Any]) -> None:
    snmp_excludes = ["RW 10", "RO 10", "RO 93", "RW93", "ANSNMP"]
    hostconf["snmp_custom"] = any(
        not any(exclude.lower() in snmp.lower() for exclude in snmp_excludes)
        for snmp in hostconf.get("snmp_custom", [])
    )


def transform_voice(hostconf: dict[str, Any]) -> None:
    hostconf["voice"] = hostconf.get("voice") or hostconf.get("voice_1", False)
    del hostconf["voice_1"]


def transform_ipv6(hostconf: dict[str, Any]) -> None:
    hostconf["ipv6"] = hostconf.get("ipv6") or hostconf.get("ipv6_1", False)
    del hostconf["ipv6_1"]


def transform_vlans(hostconf: dict[str, Any]) -> None:
    output_list = []

    exclude_l2vlans = ["database", "internal", "name"]
    if not hostconf["l2vlans"]:
        return None
    for vlan_entry in hostconf["l2vlans"]:
        if any(item in vlan_entry for item in exclude_l2vlans):
            continue
        vlans = vlan_entry.split(",")
        for vlan in vlans:
            output_list.append(vlan)

    return output_list or None


transformation_functions = {
    "domain_name": transform_domain_name,
    "pin": transform_pin,
    "snmp_custom": transform_snmp,
    "voice": transform_voice,
    "ipv6": transform_ipv6,
    "l2vlans": transform_vlans,
}


@command_or_parse(name=commands.SHOW_HOST_CONFIGURATION, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_host_configuration(command_results) -> dict[str, Any]:
    config = command_results.result
    hostconf = {}

    # Define configuration items and their processing functions
    config_items = {
        "hostname": lambda config: get_config_value(config, "hostname"),
        "bgp": lambda config: get_config_item(config, "router bgp", wildcard=True),
        "rip": lambda config: get_config_item(config, "router rip"),
        "ospf": lambda config: get_config_item(config, "router ospf", wildcard=True),
        "eigrp": lambda config: get_config_item(config, "router eigrp", wildcard=True),
        "pbr": lambda config: get_config_item(config, "ip policy route-map", global_command=False),
        # should make this so that we can pass arguments into here from the front. ip can be different per provider.
        "pin": lambda config: get_config_item(
            config, "ip nat inside source list pinverkeer-voor-nat", global_command=True
        ),
        "pin_1": lambda config: get_config_item(config, "encapsulation x25", global_command=False),
        "pin_2": lambda config: get_config_item(config, "permit ip any host 82.195.48", global_command=False),
        "pinoralr": lambda config: get_config_item(config, "ip address 10.(143|145|53).", global_command=False),
        "ipsec": lambda config: get_config_item(config, "crypto map", global_command=True, wildcard=True),
        "dhcp_server": lambda config: get_config_item(config, "ip dhcp pool", global_command=True, wildcard=True),
        "voice": lambda config: get_config_item(config, "(voice-port|dial-peer)", global_command=True, wildcard=True),
        "voice_1": lambda config: get_config_item(config, "call-manager-fallback", global_command=True),
        "tunnel": lambda config: get_config_item(config, "interface Tunnel", global_command=True),
        "vdslfirmware": lambda config: get_config_value(
            config, "firmware filename flash:", global_command=False, whitespace=False
        )
        or get_config_value(config, "firmware phy filename bootflash:", global_command=False, whitespace=False),
        "cellular": lambda config: get_config_item(config, "interface Cellular", global_command=False),
        "ipv6": lambda config: get_config_item(config, "ipv6 unicast-routing"),
        "ipv6_1": lambda config: get_config_item(config, "ipv6 address", global_command=False),
        "ip_cef": lambda config: get_config_item(config, "ip cef"),
        "ipv6_cef": lambda config: get_config_item(config, "ipv6 cef"),
        "http_server": lambda config: not get_config_item(config, "no ip http server"),
        "https_server": lambda config: not get_config_item(config, "no ip http secure-server"),
        "domain_name": lambda config: get_config_value_position(config, "ip domain name"),
        "ip_domain_lookup": lambda config: not get_config_item(config, "no ip domain lookup"),
        "ip_subnet_zero": lambda config: not get_config_item(config, "no ip subnet-zero"),
        "ip_classless": lambda config: not get_config_item(config, "no ip classless"),
        "domain_name_servers": lambda config: get_config_value_position(config, "ip name-server"),
        "service_dhcp": lambda config: not get_config_item(config, "no service dhcp"),
        "cdp": lambda config: not get_config_item(config, "no cdp run"),
        "snmp_custom": lambda config: get_config_value(config, "snmp-server community", return_list=True),
        "isdnbackup_aggregate": lambda config: get_config_value(
            config, "dialer remote-name test", global_command=False, whitespace=False
        ),
        "snmp_location": lambda config: get_config_value(config, "snmp-server location"),
        "snmp_contact": lambda config: get_config_value(config, "snmp-server contact"),
        "vtp_mode": lambda config: get_config_value(config, "vtp mode"),
        "vtp_domain": lambda config: get_config_value(config, "vtp domain"),
        "vtp_version": lambda config: get_config_value(config, "vtp version"),
        "scp": lambda config: get_config_item(config, "ip scp server enable"),
        "ip_default_gateway": lambda config: get_config_value(config, "ip default-gateway"),
        "ip_sla": lambda config: get_config_item(config, "ip sla", wildcard=True),
        "ip_nat": lambda config: get_config_item(config, "ip nat", wildcard=True),
        "netflow": lambda config: get_config_item(config, "ip netflow", wildcard=True, global_command=False),
        "nbar": lambda config: get_config_item(config, "ip nbar", wildcard=True, global_command=False),
        "multicast": lambda config: get_config_item(config, "ip multicast-routing"),
        "l2vlans": lambda config: get_config_value(config, "vlan", return_list=True),
        # Add the rest of the configuration items following the same pattern
    }

    # Process each configuration item
    for key, func in config_items.items():
        hostconf[key] = func(config)

    # Apply transformations
    for key in transformation_functions:
        transformation_functions[key](hostconf)

    return hostconf
