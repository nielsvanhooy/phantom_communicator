expected_results = {
    "interfaces": {
        "Vlan10": {
            "fhrps": {
                "1": {
                    "encryption_level": "7",
                    "encryption_string": "070C285F4D06",
                    "fhrp_description": "vpnout",
                    "group_id": "1",
                    "hsrp_timers": "msec 150 160",
                    "ips": ["1.1.1.2", "11.11.11.11 secondary", "111.111.111.111 secondary"],
                    "priority": "90",
                    "protocol": "hsrp",
                },
                "2": {
                    "encryption_level": "7",
                    "encryption_string": "070C285F4D06",
                    "group_id": "2",
                    "hsrp_preempt": True,
                    "hsrp_timers": "msec 150 msec 160",
                    "ips": ["2.2.2.2"],
                    "priority": "200",
                    "protocol": "hsrp",
                },
                "20": {
                    "encryption_string": "cisco",
                    "fhrp_description": "vpnout",
                    "group_id": "20",
                    "hsrp_timers": "150 160",
                    "ips": ["20.20.20.20", "22.22.22.22 secondary", "222.222.222.222 secondary"],
                    "priority": "100",
                    "protocol": "hsrp",
                },
            },
            "ipv4": {
                "ip": "1.1.1.1",
                "netmask": "255.255.255.0",
            },
        },
        "vlan88": {
            "fhrps": {
                "100": {
                    "encryption_level": "7",
                    "encryption_string": "070C285F4D06",
                    "fhrp_description": "hatseflats",
                    "group_id": "100",
                    "ips": ["1.1.1.2"],
                    "priority": "90",
                    "protocol": "vrrp",
                    "vrrp_timers": "50",
                },
                "110": {
                    "encryption_string": "cisco",
                    "group_id": "110",
                    "ips": ["2.2.2.2"],
                    "priority": "100",
                    "protocol": "vrrp",
                    "vrrp_learn": True,
                    "vrrp_timers": "msec 50",
                },
                "120": {
                    "group_id": "120",
                    "ips": ["3.3.3.3"],
                    "priority": "120",
                    "protocol": "vrrp",
                    "vrrp_learn": True,
                    "vrrp_preempt": False,
                },
            },
            "ipv4": {
                "ip": "88.88.88.88",
                "netmask": "255.255.255.0",
            },
        },
    },
}
