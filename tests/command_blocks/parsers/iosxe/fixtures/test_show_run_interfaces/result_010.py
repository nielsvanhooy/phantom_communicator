expected_results = [
    {
        "channel_group": {"chg": 23, "mode": "active"},
        "description": "test_of_parser",
        "flow_monitor_input": "IPv4_NETFLOW",
        "interface": "GigabitEthernet1/0/2",
        "ip_arp_inspection_limit_rate": "100",
        "ip_arp_inspection_trust": True,
        "ip_dhcp_snooping_limit_rate": "15",
        "ip_dhcp_snooping_trust": True,
        "load_interval": "30",
        "power_inline": {"max_watts": "30000", "state": "static"},
        "power_inline_port_priority": "high",
        "spanning_tree_bpdufilter": "disable",
        "spanning_tree_portfast": True,
        "switchport_block_multicast": True,
        "switchport_block_unicast": True,
        "switchport_mode": "trunk",
        "switchport_protected": True,
        "switchport_trunk_vlans": "500,821,900-905",
    }
]
