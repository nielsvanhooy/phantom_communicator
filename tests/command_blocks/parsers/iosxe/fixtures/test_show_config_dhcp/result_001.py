expected_results = [
    {
        "dhcp_excludes": {},
        "dhcp_options": {},
        "networks": {1: {"ip": "172.16.2.0", "secondary": False, "subnet_mask": "255.255.255.0"}},
        "pool_name": "hatseflats-1",
    },
    {
        "dhcp_excludes": {},
        "dhcp_options": {},
        "networks": {1: {"ip": "172.16.3.0", "secondary": False, "subnet_mask": "255.255.255.0"}},
        "pool_name": "hatseflats-2",
    },
    {
        "dhcp_excludes": {
            1: {"end": "12.1.1.10", "start": "12.1.1.10"},
            2: {"end": "12.1.1.114", "start": "12.1.1.12"},
        },
        "dhcp_options": {
            1: {"data": "10.1.1.100", "option": "150", "type": "ip"},
            2: {"data": "12.1.1.1", "option": "43", "type": "ip"},
        },
        "dns_servers": ["10.1.1.99", "10.1.1.100"],
        "domain": "nelis.nl",
        "netbios_servers": ["10.1.1.101", "10.1.1.102"],
        "networks": {
            1: {"ip": "12.1.1.0", "secondary": False, "subnet_mask": "255.255.255.0"},
            2: {"ip": "13.1.0.0", "secondary": True, "subnet_mask": "255.255.254.0"},
        },
        "pool_name": "TEST-1",
        "vrf": "lala",
    },
    {
        "dhcp_excludes": {},
        "dhcp_options": {
            1: {
                "data": "010a.5369.656d.656e.7300.0000.0204.0000.0258.0317.7364.6c70.3a2f.2f31.3732.2e31.372e.302e.323a.3138.3434.33ff",
                "option": "43",
                "type": "hex",
            }
        },
        "dns_servers": ["10.31.1.1", "10.31.107.253"],
        "domain": "test-voice.local",
        "gateway": "172.19.0.254",
        "networks": {1: {"ip": "172.19.0.0", "secondary": False, "subnet_mask": "255.255.0.0"}},
        "pool_name": "BFR-test-voice",
    },
    {
        "dhcp_excludes": {1: {"end": "10.1.1.20", "start": "10.1.10.2"}},
        "dhcp_options": {1: {"data": "139.156.73.67", "option": "150", "type": "ip"}},
        "dns_servers": ["213.162.171.133", "213.162.171.134"],
        "gateway": "10.1.10.1",
        "networks": {1: {"ip": "10.1.10.0", "secondary": False, "subnet_mask": "255.255.255.0"}},
        "pool_name": "test-company-(CGR)",
    },
    {
        "boot_file": "testfile",
        "dhcp_excludes": {},
        "dhcp_options": {1: {"data": '"10.12.1.10"', "option": "66", "type": "ascii"}},
        "dns_servers": ["10.100.1.5"],
        "domain": "woonzorg.local",
        "gateway": "10.111.10.1",
        "networks": {1: {"ip": "10.111.10.0", "secondary": False, "subnet_mask": "255.255.255.0"}},
        "pool_name": "cxbeh",
    },
    {
        "dhcp_excludes": {},
        "dhcp_options": {
            1: {"data": "3a02.14ff", "option": "43", "type": "hex"},
            2: {"data": "'10.80.3.33' '40003'", "option": "201", "type": "ascii"},
            3: {"data": "10.80.3.33", "option": "202", "type": "ip"},
        },
        "dns_servers": ["10.80.2.4", "10.80.2.5"],
        "domain": "corp.csu.lan",
        "gateway": "10.222.254.254",
        "lease_time": "8",
        "networks": {1: {"ip": "10.222.0.0", "secondary": False, "subnet_mask": "255.255.0.0"}},
        "pool_name": "DHCP_TEST1",
    },
    {
        "dhcp_excludes": {},
        "dhcp_options": {
            1: {
                "data": "id:ipphone.mitel.com;call_srv=143.0.0.1;vlan=40;l2p=6;dscp=46;sw_tftp=143.0.0.1",
                "option": "43",
                "type": "ascii",
            }
        },
        "gateway": "172.16.100.200",
        "networks": {1: {"ip": "172.16.100.0", "secondary": False, "subnet_mask": "255.255.255.0"}},
        "pool_name": "Mitel",
    },
    {
        "dhcp_excludes": {},
        "dhcp_options": {
            1: {"data": "172.24.1.2", "option": "186", "type": "ip"},
            2: {"data": "01bb", "option": "190", "type": "hex"},
            3: {"data": '"172.24.1.2"', "option": "161", "type": "ascii"},
            4: {"data": '"wdmserverrapport"', "option": "184", "type": "ascii"},
            5: {"data": '"DellWyse"', "option": "185", "type": "ascii"},
        },
        "gateway": "130.1.41.253",
        "networks": {1: {"ip": "130.1.41.0", "secondary": False, "subnet_mask": "255.255.255.0"}},
        "pool_name": "SUVM1202",
    },
]
