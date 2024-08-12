expected_results = {
    "interfaces": {
        "ATM0/2/0": {"shutdown": True},
        "Ethernet0/2/0": {"negotiation_auto": False, "shutdown": True},
        "GigabitEthernet0/0/0": {
            "description": "Connection toblabla " "#  #",
            "ipv4": {"ip": "10.121.67.157", "netmask": "255.255.255.252"},
            "media_type": "rj45",
            "negotiation_auto": False,
            "output_policy": "MVLAN",
            "speed": 100,
        },
        "GigabitEthernet0/1/0": {
            "description": "Connection to " "Customer VOICE LAN",
            "hold_queue_in": 500,
            "hold_queue_out": 100,
            "switchport_access_vlan": "215",
        },
        "GigabitEthernet0/1/1": {
            "description": "Connection to " "Customer DATA LAN",
            "hold_queue_in": 500,
            "hold_queue_out": 100,
            "switchport_access_vlan": "115",
        },
        "GigabitEthernet0/1/2": {"shutdown": True},
        "GigabitEthernet0/1/3": {"shutdown": True},
        "Loopback0": {"ipv4": {"ip": "10.126.67.25", "netmask": "255.255.255.255"}},
        "Vlan1": {"shutdown": True},
        "Vlan115": {
            "acl": {"inbound": {"acl_name": "160", "direction": "in"}},
            "description": "VLAN for Customer DATA LAN",
            "input_policy": "Coloring_realtime",
            "ipv4": {"ip": "10.18.1.1", "netmask": "255.255.255.0"},
        },
        "Vlan215": {
            "acl": {"inbound": {"acl_name": "160", "direction": "in"}},
            "description": "VLAN for Customer VOICE LAN",
            "input_policy": "Coloring_realtime",
            "ip_helpers": ["10.15.1.11"],
            "ipv4": {"ip": "10.18.2.1", "netmask": "255.255.255.0"},
        },
    }
}
