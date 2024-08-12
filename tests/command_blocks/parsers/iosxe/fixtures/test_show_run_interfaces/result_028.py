expected_results = {
    "interfaces": {
        "Vlan10": {
            "acl": {
                "inbound": {
                    "acl_name": "171",
                    "direction": "in",
                },
                "outbound": {
                    "acl_name": "171",
                    "direction": "out",
                },
            },
            "description": "### DATA ###",
            "input_policy": "Coloring-traffic1",
            "ip_helpers": ["10.101.65.76", "10.101.4.10"],
            "ipv4": {
                "ip": "10.0.145.254",
                "netmask": "255.255.255.0",
            },
            "ipv4_secondaries": {
                "10.53.173.137": {
                    "ip": "10.53.173.137",
                    "netmask": "255.255.255.248",
                    "primary": False,
                },
            },
        },
    },
}
