import re
from typing import Union

from .command import Command


def commands_list(commands) -> Union[list[Command], list]:
    """
    Create a list of commands

    :param commands:
    :return:
    """
    cmd_list = []
    for c in commands:
        cmd_list.append(Command(c))
    return cmd_list


def get_match(data, regex, n=1):
    """
    Get the match of the data using the regex

    :param data:
    :param regex:
    :return:
    """
    try:
        return re.search(regex, data).group(n)
    except AttributeError:
        return None


def generate_dict(data):
    # generates a dict from bulk snmp info.
    # it combines based on the last 2 digits from the oid
    result = {}
    for oid, desc in data:
        parts = oid.split(".")
        last_segment = parts[-1]
        preceding_segment = parts[-2]
        if last_segment not in result:
            result[last_segment] = {}
        result[last_segment][preceding_segment] = f'"{desc}"'
    return result


def is_prefix_in_list(oid, prefix_list):
    for prefix in prefix_list:
        if oid.startswith(prefix):
            return True
    return False


def convert_to_epoch(uptime_dict: dict[str, int]) -> int:
    # Conversion factors for each unit to seconds
    conversion_factors = {
        "years": 31536000,
        "weeks": 604800,
        "days": 86400,
        "hours": 3600,
        "minutes": 60,
        "seconds": 1,
    }

    # Calculate total epoch time by summing the products of values and conversion factors
    return sum(uptime_dict.get(unit, 0) * factor for unit, factor in conversion_factors.items())
