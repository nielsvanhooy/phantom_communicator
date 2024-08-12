expected_results = {
    "interfaces": {
        "ATM0/3/0.32": {
            "pvc_vp": 2,
            "pvc_vc": 32,
            "pvc_ubr": "1024 48",
            "output_policy": "policy-cbwfq",
            "dialer_pool": "1",
        },
        "Dialer0": {
            "mtu": 1500,
            "src_ip": "Loopback0",
            "encapsulation_ppp": True,
            "dialer_pool": "1",
            "chap_hostname": "hostname",
            "chap_password": "password",
            "chap_encryption": 0,
        },
        "Dialer1": {
            "mtu": 1500,
            "src_ip": "Loopback1",
            "encapsulation_ppp": True,
            "dialer_pool": "2",
            "chap_hostname": "hostname",
            "chap_password": "08345F4B1B48",
            "chap_encryption": 7,
        },
        "Ethernet0/3/0.3": {
            "description": "Connection to TEST",
            "encapsulation_dot1q": "3",
            "dialer_pool": "1",
            "pppoe_max_payload": 1500,
        },
        "GigabitEthernet0/0/1.954": {
            "acl": {"inbound": {"acl_name": "160", "direction": "in"}},
            "description": "Vlan for Customer",
            "encapsulation_dot1q": "954",
            "vrf": "cisco",
            "ipv4": {
                "ip": "172.18.132.252",
                "netmask": "255.255.255.0",
            },
            "ip_helpers": ["158.67.245.51", "158.67.245.53"],
        },
        "Cellular0/2/0": {
            "description": "Wireless Access to TEST",
            "ip_negotiated": True,
            "load_interval": "30",
            "output_policy": "policy-cbwfq",
        },
    }
}
