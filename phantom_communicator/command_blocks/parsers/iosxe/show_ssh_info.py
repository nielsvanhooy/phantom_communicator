import re
from typing import Any

from phantom_communicator.command_blocks import constants as commands
from phantom_communicator.command_blocks.decorators import command_or_parse


@command_or_parse(name=commands.SHOW_SSH_INFO, vendor=commands.CISCO, os="iosxe", type="parse_command")
def parse_show_ssh_info(command_results) -> dict[str, Any | None]:
    data = command_results.result

    ssh_version = r"SSH Enabled -\s+(.*)"  # noqa: W605,E501
    ssh_auth_pubkey_algorithms = r"Authentication Publickey Algorithms:(.*)"
    ssh_hostkey_algorithms = r"Hostkey Algorithms:(.*)"
    ssh_encryp_algorithms = r"Encryption Algorithms:(.*)"
    ssh_mac_algorithms = r"MAC Algorithms:(.*)"
    ssh_dh_size = r"Diffie Hellman key size :\s+(.*)"  # noqa: W605,E501

    get_ssh_version = re.findall(ssh_version, data)
    get_ssh_auth_pubkey = re.findall(ssh_auth_pubkey_algorithms, data)
    get_ssh_hostkey_algorithms = re.findall(ssh_hostkey_algorithms, data)
    get_ssh_encryp_algoritms = re.findall(ssh_encryp_algorithms, data)
    get_ssh_mac_algoritms = re.findall(ssh_mac_algorithms, data)
    get_ssh_dh_size = re.findall(ssh_dh_size, data)

    ssh_dict = {
        "ssh_version": get_ssh_version[0] if get_ssh_version else None,
        "ssh_auth_pubkey": (get_ssh_auth_pubkey[0].split(",") if get_ssh_auth_pubkey else None),
        "ssh_hostkey_algorithms": (get_ssh_hostkey_algorithms[0].split(",") if get_ssh_hostkey_algorithms else None),
        "ssh_encryp_algorithms": (get_ssh_encryp_algoritms[0].split(",") if get_ssh_encryp_algoritms else None),
        "ssh_mac_algorithms": (get_ssh_mac_algoritms[0].split(",") if get_ssh_mac_algoritms else None),
        "ssh_dh_size": get_ssh_dh_size[0] if get_ssh_dh_size else None,
    }
    return ssh_dict
