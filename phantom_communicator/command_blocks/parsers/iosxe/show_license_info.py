import re

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_LICENSE, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_license_info(command_results) -> list:
    data = command_results.result

    license_list = data.split("Index")
    license_list.pop(0)
    # we split the output on the word Index
    # so that i have feature and state of the feature in seperate lists
    # below regex for feature is after the split
    license_feature = r"\d Feature: (.*)"
    license_state = r"License State:\s+(.*)"

    feature_state_list = []
    for index in license_list:
        get_license_feature = re.findall(license_feature, index)
        get_license_state = re.findall(license_state, index)
        if len(get_license_state) == 0:
            get_license_state = ["Base License has no state"]

        license_dict = {
            "feature": get_license_feature[0].rstrip(),
            "state": get_license_state[0].rstrip(),
        }
        feature_state_list.append((license_dict))
    return feature_state_list
