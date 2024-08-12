expected_results = {
    "interfaces": {
        "GigabitEthernet0/0/5": {
            "description": "Cascade to DEVICE-Fa4 # Multi-VLAN #",
            "encapsulation_dot1q": "1994",
            "media_type": "auto-select",
            "negotiation_auto": True,
            "service_instances": {
                "1990": {
                    "bridge_domain": "1990",
                    "dot1q": "1990",
                    "service_instance": "1990",
                    "service_instance_trunked": False,
                },
                "1991": {
                    "bridge_domain": "1991",
                    "dot1q": "1991",
                    "service_instance": "1991",
                    "service_instance_trunked": False,
                },
                "1992": {
                    "bridge_domain": "1992",
                    "dot1q": "1992",
                    "service_instance": "1992",
                    "service_instance_trunked": False,
                },
                "1994": {
                    "bridge_domain": "1994",
                    "dot1q": "1994",
                    "service_instance": "1994",
                    "service_instance_trunked": False,
                },
            },
        },
        "GigabitEthernet0/0/6": {
            "load_interval": "30",
            "media_type": "rj45",
            "negotiation_auto": False,
            "service_instances": {
                "1": {
                    "dot1q": "2,77,88,200,202-204,207,209,211,220,601,700,702-710,715,720-750,843,851-852,859",
                    "service_instance": "1",
                    "service_instance_trunked": True,
                },
            },
            "speed": 100,
        },
    },
}
