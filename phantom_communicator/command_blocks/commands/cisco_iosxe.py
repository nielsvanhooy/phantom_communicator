from phantom_communicator.command_blocks.command import Command, CommandConstructor
from phantom_communicator.command_blocks.decorators import command, return_config
from phantom_communicator.command_blocks.snmp_command import SNMPCommand
from phantom_communicator.command_blocks import constants as commands


@command(name=commands.ENABLE, vendor=commands.CISCO, os="iosxe")
def enable(password) -> Command:
    """
    Probably won't be used anymore. The netmiko library handles its own enable
    method.
    :param password:
    :return:
    """
    return Command(f"enable\n{password}\n")


@command(name=commands.ENTER_CONFIGURATION_MODE, vendor=commands.CISCO, os="iosxe")
def enter_configuration_mode() -> Command:
    return Command("configure terminal")


@command(name=commands.EXIT_CONFIGURATION_MODE, vendor=commands.CISCO, os="iosxe")
def exit_configuration_mode() -> Command:
    return Command("end")


@command(name=commands.SETUP_SESSION, vendor=commands.CISCO, os="iosxe")
def setup_session() -> Command:
    return Command("terminal length 0")


@command(name=commands.SHOW_UPTIME, vendor=commands.CISCO, os="iosxe")
@command(name=commands.SHOW_VERSION, vendor=commands.CISCO, os="iosxe")
def show_ver(*args, **kwargs) -> Command:
    return Command("show ver")


@command(name=commands.SHOW_SOFTWARE, vendor=commands.CISCO, os="iosxe")
def show_software(*args, **kwargs) -> list:
    return [Command("show ver"), SNMPCommand("1.3.6.1.4.1.9.2.1.73.0")]


@command(name=commands.SHOW_HOSTNAME, vendor=commands.CISCO, os="iosxe")
def show_hostname() -> Command:
    return Command("show running-config | i ^hostname.*$")


@command(name=commands.RESET_STARTUP_CONFIG, vendor=commands.CISCO, os="iosxe")
def reset_startup_config(config_file) -> Command:
    return Command(command=f"copy flash:/{config_file} " f"startup-config")


@command(name=commands.REBOOT, vendor=commands.CISCO, os="iosxe")
@return_config()
def reboot() -> list:
    return ["reload\n"]


@command(name=commands.REBOOT_IN, vendor=commands.CISCO, os="iosxe")
@return_config()
def reboot_in() -> list:
    return ["reload in 1\n"]


@command(name=commands.SHOW_RUNNING_CONFIG, vendor=commands.CISCO, os="iosxe")
def show_running_config() -> Command:
    return Command("show running-config")


@command(name=commands.SHOW_STARTUP_CONFIG, vendor=commands.CISCO, os="iosxe")
def show_startup_config() -> Command:
    return Command("show startup-config")


@command(name=commands.SHOW_MEMORY, vendor=commands.CISCO, os="iosxe")
@return_config()
def show_memory(*args) -> list:
    return ["show memory statistics", "sh flash: | i bytes"]


@command(name=commands.SHOW_INVENTORY, vendor=commands.CISCO, os="iosxe")
def show_inventory(*args) -> list:
    return [
        # begin inventory
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.2"),  # entPhysicalDescr
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.5"),  # entPhysicalClass
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.7"),  # entPhysicalName
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.8"),  # entPhysicalHardwareRev
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.9"),  # entPhysicalFirmwareRev
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.10"),  # entPhysicalSoftwareRev
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.11"),  # entPhysicalSerialNum
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.12"),  # entPhysicalMfgName
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.13"),  # entPhysicalModelName
        SNMPCommand("1.3.6.1.2.1.47.1.1.1.1.16"),  # entPhysicalIsFRU
        # end inventory
    ]


@command(name=commands.SHOW_SSH_INFO, vendor=commands.CISCO, os="iosxe")
def show_ssh_info(*args) -> Command:
    return Command("show ip ssh")


@command(name=commands.SHOW_LICENSE, vendor=commands.CISCO, os="iosxe")
def show_license_info(*args) -> Command:
    return Command("show license")


@command(name=commands.SHOW_FEATURESET, vendor=commands.CISCO, os="iosxe")
def show_featureset(*args) -> list:
    return [SNMPCommand("1.3.6.1.4.1.9.9.25.1.1.1.2.4")]


@command(name=commands.VERIFY_MD5, vendor=commands.CISCO, os="iosxe")
def verify_md5(filename, md5) -> Command:
    return Command(f"verify /md5 {filename} {md5}", timeout=600)


@command(name=commands.SET_BOOT_IOS, vendor=commands.CISCO, os="iosxe")
@return_config()
def set_boot_ios(filename, backup=None) -> list:
    command_list = [
        "no boot system",
        f"boot system flash:{filename}",
    ]

    if backup:
        command_list.append(f"boot system flash:{backup}")

    return command_list


# @command(
#     name=commands.SET_BOOT_IOS,
#     vendor=commands.CISCO,
#     model=constants.SUPPORTED_MODEL_1113,
# )
# @command(
#     name=commands.SET_BOOT_IOS,
#     vendor=commands.CISCO,
#     model=constants.SUPPORTED_MODEL_1117,
# )
# @command(
#     name=commands.SET_BOOT_IOS,
#     vendor=commands.CISCO,
#     model=constants.SUPPORTED_MODEL_ISR_4331,
# )
# @command(
#     name=commands.SET_BOOT_IOS,
#     vendor=commands.CISCO,
#     model=constants.SUPPORTED_MODEL_ISR_4431,
# )
# @command(
#     name=commands.SET_BOOT_IOS,
#     vendor=commands.CISCO,
#     model=constants.SUPPORTED_MODEL_ISR_4451,
# )
# @command(
#     name=commands.SET_BOOT_IOS,
#     vendor=commands.CISCO,
#     model=constants.SUPPORTED_MODEL_ASR920,
# )
# @return_config()
# def set_boot_ios(filename, backup=None) -> list:
#     command_list = [
#         "no boot system",
#         f"boot system bootflash:{filename}",
#     ]
#
#     if backup:
#         command_list.append(f"boot system bootflash:{backup}")
#
#     return command_list


@command(name=commands.SAVE_CONFIG, vendor=commands.CISCO, os="iosxe")
def save_config() -> list:
    command_list = [
        Command("write mem"),
        # Extra newline in case there is a confirmation for the NVRAM prompt
        Command("\n", timeout=120),
    ]

    # old but not obsolete :)
    # command_list = [
    #     Command("copy running-config startup-config"),
    #     Command("startup-config", timeout=120),
    #     # Extra newline in case there is a confirmation for the NVRAM prompt
    #     Command("\n", timeout=120),
    # ]

    return command_list


@command(name=commands.SEND_SYSLOG, vendor=commands.CISCO, os="iosxe")
@return_config()
def send_syslog(message, level=5) -> list:
    return [f"send log {level} {message}"]


@command(name=commands.GET_BOOT_STATEMENTS, vendor=commands.CISCO, os="iosxe")
def get_boot_statements() -> Command:
    return Command("show startup | i ^boot", timeout=120)


@command(name=commands.LIST_SOFTWARE_FILES, vendor=commands.CISCO, os="iosxe")
def list_boot_files() -> Command:
    return Command("dir *.bin", timeout=120)


@command(name=commands.DELETE_FILE, vendor=commands.CISCO, os="iosxe")
def delete_file(filename) -> Command:
    return Command(f"delete /force flash:{filename}", timeout=120)


@command(name=commands.REMOVE_EEM_SSH_SCRIPT, vendor=commands.CISCO, os="iosxe")
@return_config()
def remove_eem_ssh_script() -> list:
    return [
        "conf t",
        "no event manager applet EEM_SSH_Keygen",
        "exit",
    ]


@command(name=commands.SHOW_CELLULAR, vendor=commands.CISCO, os="iosxe")
class ShowCellularCommand(CommandConstructor):
    @staticmethod
    def get_cellulars(cpe) -> list:
        return [
            item
            for item in cpe.wan_ports.all()
            if (
                    item.product_configuration_wan.access_type == "lte"
                    and not item.shutdown
            )
        ]

    def is_eligible_to_execute(self, cpe) -> bool:
        # any active cellular present ?
        return True if self.get_cellulars(cpe) else False

    def get_commands(self, cpe) -> Command:
        cellular = self.get_cellulars(cpe)[0]
        interface = str(
            cellular.product_configuration_wan.port_name
            + " "
            + cellular.product_configuration_wan.port_number
        )
        return Command(f"show {interface} all")


@command(name=commands.SHOW_CONTROLLER, vendor=commands.CISCO, os="iosxe")
class ShowControllerCommand(CommandConstructor):
    @staticmethod
    def get_controller(cpe) -> list:
        return [
            item
            for item in cpe.wan_ports.all()
            if (
                    "vdsl" in item.product_configuration_wan.access_type
                    and not item.shutdown
            )
        ]

    def is_eligible_to_execute(self, cpe) -> bool:
        # any active DSL controller present ?
        return True if self.get_controller(cpe) else False

    def get_commands(self, cpe) -> Command:
        dsl = self.get_controller(cpe)[0]
        interface = str("VDSL " + dsl.product_configuration_wan.port_number)
        return Command(f"show controller {interface}")