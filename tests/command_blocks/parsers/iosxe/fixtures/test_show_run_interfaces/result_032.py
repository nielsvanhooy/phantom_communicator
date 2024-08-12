expected_results = {
    "interfaces": {
        "GigabitEthernet0/0/5": {
            "media_type": "auto-select",
            "negotiation_auto": True,
            "hold_queue_in": 500,
            "hold_queue_out": 100,
            "service_instances": {
                "11": {
                    "service_instance": "11",
                    "description": "belongs to BDI11 TEST",
                    "dot1q": "11",
                    "bridge_domain": "11",
                    "service_instance_trunked": False,
                },
                "15": {
                    "service_instance": "15",
                    "description": "belongs to BDI15 TEST2",
                    "dot1q": "15",
                    "bridge_domain": "15",
                    "service_instance_trunked": False,
                },
                "21": {
                    "service_instance": "21",
                    "description": "belongs to BDI21 TEST3",
                    "dot1q": "21",
                    "bridge_domain": "21",
                    "service_instance_trunked": False,
                },
                "99": {
                    "service_instance": "99",
                    "description": "belongs to BDI99 TEST4",
                    "dot1q": "99",
                    "bridge_domain": "99",
                    "service_instance_trunked": False,
                },
            },
        }
    }
}
