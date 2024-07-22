import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse
from phantom_communicator.command_blocks.helpers import crypto7decrypt


@command_or_parse(name=commands.SHOW_CELLULAR, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_cellular(command_results) -> dict[str, Any]:
    data = command_results.result

    properties = get_properties(data)

    profile = get_profile(data)
    properties["username"] = profile["username"] if profile else ""
    properties["password"] = crypto7decrypt(profile["password"]) if profile else ""
    properties["authentication"] = profile["authentication"] if profile else ""
    properties["apn"] = profile["apn"] if profile else ""

    wireless_dict = {
        "imei": properties["imei"],
        "imsi": properties["imsi"],
        "iccid": properties["iccid"],
        "simnr": properties["iccid"][6:18],
        "network": properties["network"],
        "network_selection_method": properties["network_selection_mode"],
        "packet_service": properties["packet_service"],
        "current_service": properties["current_service"],
        "current_service_status": properties["current_service_status"],
        "band_select": properties["band_select"],
        "modem_temperature": properties["modem_temperature"],
        "modem_firmware_version": properties["modem_firmware_version"],
        "ip_address": properties["ip_address"],
        "primary_dns": properties["primary_dns"],
        "secondary_dns": properties["secondary_dns"],
        "current_rssi": properties["rssi"],
        "current_rsrp": properties["rsrp"],
        "current_rsrq": properties["rsrq"],
        "current_snr": properties["snr"],
        "sim_status": properties["sim_status"],
        "mobile_authentication": properties["authentication"],
        "mobile_username": properties["username"],
        "mobile_password": properties["password"],
        "mobile_apn": properties["apn"],
    }
    return wireless_dict


def get_properties(command_output):
    properties = {}
    regex_list = (
        (r"\(IMEI\) = (.*)", "imei", str),
        (r"\(IMSI\) = (.*)", "imsi", str),
        (r"\(ICCID\) = (.*)", "iccid", str),
        (r"Network Selection Mode = (.*)", "network_selection_mode", str),
        (r"Packet Service = (.*)", "packet_service", list),
        (r"Current Service = (.*)", "current_service", str),
        (r"Current Service Status = (.*)", "current_service_status", str),
        (r"Modem Firmware Version = (.*)", "modem_firmware_version", str),
        (r"Current Modem Temperature = (.*)", "modem_temperature", str),
        (r"IP address = (.*)", "ip_address", str),
        (r"Primary DNS address = (.*)", "primary_dns", str),
        (r"Secondary DNS address = (.*)", "secondary_dns", str),
        (r"Current RSSI = (.*)", "rssi", str),
        (r"Current RSRP = (.*)", "rsrp", str),
        (r"Current RSRQ = (.*)", "rsrq", str),
        (r"SIM Status = (.*)", "sim_status", str),
        (r"Current SNR = (.*)", "snr", str),
        (r"Network = (.*)", "network", str),
        (r"Band Selected = (.*)", "band_select", list),
    )

    for matching_profile in regex_list:
        # This needs to be a regular find:
        # Empty value should be empty string, not an empty list
        # Why was this done in the first place?
        # What's the impact of changing this?

        regex, target_key, target_type = matching_profile

        match = re.search(regex, command_output)

        if match:
            value = match[1].strip()
            if isinstance(target_type, list):
                match = [] if len(value) == 0 else [value]
            else:
                match = value
        else:
            match = target_type()

        properties[target_key] = match
    return properties


def get_profile(command_output):
    profile = {}

    regex = r"ACTIVE\*([\S\s]*?)profile"
    match = re.findall(regex, command_output, re.MULTILINE)

    regex_list = (
        (r"Username = (.*)", "username"),
        (r"Password = (.*)", "password"),
        (r"Authentication = (.*)", "authentication"),
        (r"Access Point Name \(APN\) = (.*)", "apn"),
    )

    if match and "Username:" in match[0]:
        regex_list = (
            (r"Username: (.*)", "username"),
            (r"Password: (.*)", "password"),
            (r"Authentication = (.*)", "authentication"),
            (r"Access Point Name \(APN\) = (.*)", "apn"),
        )

    regex = r"ACTIVE\*([\S\s]*?)profile"
    match = re.findall(regex, command_output, re.MULTILINE)

    if not match:
        return None

    for regex in regex_list:
        regex_result = re.findall(regex[0], match[0])
        if regex_result:
            regex_result = regex_result[0].strip()
        profile[regex[1]] = regex_result

    return profile
