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


def crypto7decrypt(enc_pwd: str) -> str:
    # referentie: https://github.com/axcheron/cisco_pwdecrypt/blob/master/cisco_pwdecrypt.py

    xlat = [
        0x64,
        0x73,
        0x66,
        0x64,
        0x3B,
        0x6B,
        0x66,
        0x6F,
        0x41,
        0x2C,
        0x2E,
        0x69,
        0x79,
        0x65,
        0x77,
        0x72,
        0x6B,
        0x6C,
        0x64,
        0x4A,
        0x4B,
        0x44,
        0x48,
        0x53,
        0x55,
        0x42,
        0x73,
        0x67,
        0x76,
        0x63,
        0x61,
        0x36,
        0x39,
        0x38,
        0x33,
        0x34,
        0x6E,
        0x63,
        0x78,
        0x76,
        0x39,
        0x38,
        0x37,
        0x33,
        0x32,
        0x35,
        0x34,
        0x6B,
        0x3B,
        0x66,
        0x67,
        0x38,
        0x37,
    ]

    password = enc_pwd
    try:
        index = int(enc_pwd[:2])
        enc_pwd = enc_pwd[2:].rstrip()
        pwd_hex = [enc_pwd[x : x + 2] for x in range(0, len(enc_pwd), 2)]
        cleartext = [chr(xlat[index + i] ^ int(pwd_hex[i], 16)) for i in range(len(pwd_hex))]
        return "".join(cleartext)

    except (IndexError, ValueError):
        return password
