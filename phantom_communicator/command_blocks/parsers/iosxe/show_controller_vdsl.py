import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_CONTROLLER, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_controller(command_results) -> dict[str, Any]:
    data = command_results.result

    properties = {}
    regex_list = [
        (r"Controller .* (DOWN)", "status"),
        (r"Daemon Status:[ \t]+(.*)", "daemonstatus"),
        (r"Modem Status:[ \t]+(.*)", "modemstatus"),
        (r"Line Attenuation:[ \t]+(.* dB)[ \t]+(.* dB)", "lineattenuation"),
        (r"Actual Power:[ \t]+(.* dBm)[ \t]+(.* dBm)", "actualpower"),
        (r"Signal Attenuation:[ \t]+(.* dB)[ \t]+(.* dB)", "signalattenuation"),
        (r"Noise Margin:[ \t]+(.* dB)[ \t]+(.* dB)", "noisemargin"),
        (r"Attainable Rate:[ \t]+(.* kbits/s)[ \t]+(.* kbits/s)", "attainablerate"),
        (r"Serial Number Far:[ \t]+(.*)", "serialnumberfar"),
        (r"DSL Config Mode:[ \t]+(.*)", "dslconfigmode"),
        (r"TC Mode:[ \t]+(.*)", "tcmode"),
    ]

    data = data.replace("\t", " ")
    data = data.replace("\r\n", "\n")

    for regex in regex_list:
        match = re.findall(regex[0], data)
        properties[regex[1]] = ""
        if not match:
            continue
        properties[regex[1]] = match[0]

    if properties["status"].lower() == "down":
        return {}
    controller_dict = {
        "daemon_status": properties["daemonstatus"],
        "modem_status": properties["modemstatus"],
        "lineattenuation": {
            "a-end": {
                "value": properties["lineattenuation"][0].split()[0],
                "unit": properties["lineattenuation"][0].split()[1],
            },
            "b-end": {
                "value": properties["lineattenuation"][1].split()[0],
                "unit": properties["lineattenuation"][1].split()[1],
            },
        },
        "actualpower": {
            "a-end": {
                "value": properties["actualpower"][0].split()[0],
                "unit": properties["actualpower"][0].split()[1],
            },
            "b-end": {
                "value": properties["actualpower"][1].split()[0],
                "unit": properties["actualpower"][1].split()[1],
            },
        },
        "signalattenuation": {
            "a-end": {
                "value": properties["signalattenuation"][0].split()[0],
                "unit": properties["signalattenuation"][0].split()[1],
            },
            "b-end": {
                "value": properties["signalattenuation"][1].split()[0],
                "unit": properties["signalattenuation"][1].split()[1],
            },
        },
        "noisemargin": {
            "a-end": {
                "value": properties["noisemargin"][0].split()[0],
                "unit": properties["noisemargin"][0].split()[1],
            },
            "b-end": {
                "value": properties["noisemargin"][1].split()[0],
                "unit": properties["noisemargin"][1].split()[1],
            },
        },
        "attainablerate": {
            "a-end": {
                "value": properties["attainablerate"][0].split()[0],
                "unit": properties["attainablerate"][0].split()[1],
            },
            "b-end": {
                "value": properties["attainablerate"][1].split()[0],
                "unit": properties["attainablerate"][1].split()[1],
            },
        },
        "serialnumberfar": properties["serialnumberfar"],
        "dslconfigmode": properties["dslconfigmode"],
        "tcmode": properties["tcmode"],
    }

    return controller_dict
