from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks.helpers import generate_dict


@command_or_parse(name=commands.SHOW_INVENTORY, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_inventory(command_results) -> list:
    """
    Parses SNMP command results to extract inventory information.

    :param command_results: The result from executing an SNMP command.
    :param vendor: The vendor name, defaults to 'cisco'.
    :return: A list of dictionaries, each representing an inventory item.
    """
    if not command_results.result or command_results.cmd_type != "snmp":
        return []

    matches_dict = generate_dict(command_results.result)
    if not matches_dict:
        return []

    return [
        {
            "sortorder": index + 1,
            "descr": item[1].get("2", ""),
            "modelname": item[1].get("13", ""),
            "serialnumber": item[1].get("11", ""),
            "class": item[1].get("5", ""),
            "name": item[1].get("7", ""),
            "hardwarerev": item[1].get("8", ""),
            "firmwarerev": item[1].get("9", ""),
            "softwarerev": item[1].get("10", ""),
            "mfgname": item[1].get("12", ""),
            "fru": item[1].get("16", ""),
        }
        for index, item in enumerate(matches_dict.items())
    ]
