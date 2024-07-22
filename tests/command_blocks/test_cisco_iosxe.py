from phantom_communicator.command_blocks.command_and_parse import CommandParser
from phantom_communicator.communicators.base import Communicator
from tests.command_blocks.test_data.loader import load_test_data


def test_basic(cb_cisco):
    assert cb_cisco.show_version().command == "show ver"
    assert cb_cisco.setup_session().command == "terminal length 0"


async def test_show_ver():
    test_data_name = "show_ver_iosxe"
    testdata = load_test_data(test_data_name)

    # test_parsers.show_version().parser

    communicator = Communicator.factory(host="192.168.1.50", username="lagen008", password="lagen008", os="iosxe")
    communicator.community_string = "7QuIvTihXlxkEicZl8SAinw6"
    async with communicator as conn:
        data = await conn.execute_and_parse_commands(
            [
                # "show_config_dhcp",
                # "show_version",
                # "show_software",
                # "show_inventory",
                # "show_uptime",
                # "show_license_info",
                # "show_ssh_info",
                ("show_controller_vdsl", [0]),
                # "show_memory",
                # "show_featureset",
                ("show_cellular", [0, 0]),
            ],
            use_cache=True,
        )
        print(data)
        data_two = await conn.send_command("show int desc")
        data_three = await conn.send_commands(["show int desc", "show ip int brief"])
    lala = "loeloe"
