expected_results = [
    {
        "hold_queue_in": 500,
        "hold_queue_out": 100,
        "interface": "GigabitEthernet0/0/5",
        "media_type": "auto-select",
        "negotiation_auto": True,
        "service_instances": {
            "11": {
                "bridge_domain": "11",
                "description": "belongs to BDI11 TEST",
                "dot1q": "11",
                "service_instance": "11",
                "service_instance_trunked": False,
            },
            "15": {
                "bridge_domain": "15",
                "description": "belongs to BDI15 TEST2",
                "dot1q": "15",
                "service_instance": "15",
                "service_instance_trunked": False,
            },
            "21": {
                "bridge_domain": "21",
                "description": "belongs to BDI21 TEST3",
                "dot1q": "21",
                "service_instance": "21",
                "service_instance_trunked": False,
            },
            "99": {
                "bridge_domain": "99",
                "description": "belongs to BDI99 TEST4",
                "dot1q": "99",
                "service_instance": "99",
                "service_instance_trunked": False,
            },
        },
    }
]
