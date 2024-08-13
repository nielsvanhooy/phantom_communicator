expected_results = [
    {
        "host_reachability_protocol": "bgp",
        "interface": "nve1",
        "member_vni": {
            "20011": {"ingress_replication": {"enabled": True}},
            "20012": {"ingress_replication": {"enabled": True}, "local_routing": True},
            "20013": {"local_routing": True, "mcast_group": "239.1.1.3"},
            "20014": {"mcast_group": "239.1.1.4"},
            "30000": {"vrf": "red"},
        },
        "source_interface": "Loopback1",
    }
]
