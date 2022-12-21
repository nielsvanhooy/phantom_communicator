def test_make_connection_scrapli():
    from scrapli.driver.core import IOSXEDriver

    my_device = {
        "host": "10.17.28.194",
        "auth_username": "lagen008",
        "auth_password": "lagen008",
        "auth_strict_key": False,
    }

    with IOSXEDriver(**my_device) as conn:
        response = conn.send_command("show ip route")
        structured_result = response.genie_parse_output()
        print(structured_result)


# def test_network_extractor_scrapli():
#     import time
#
#     start_time = time.time()
#     from scrapli.driver.core import IOSXEDriver
#
#     extraction_settings = {"genie_commands": ["show ip route"]}
#     platform = "iosxe"
#
#     my_device = {
#         "host": "10.17.28.194",
#         "auth_username": "lagen008",
#         "auth_password": "lagen008",
#         "auth_strict_key": False,
#     }
#
#     with IOSXEDriver(**my_device) as communicator_session:
#         extractor = NetworkDeviceExtractor(platform, communicator_session, **extraction_settings)
#         extracted_data = extractor.extract_all()
#         print(extracted_data)
#     print("My program took", time.time() - start_time, "to run")
