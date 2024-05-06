import asyncio
from collections import namedtuple
from typing import List, Literal, Optional, Tuple, Union

from asyncssh import ConnectionLost
from scrapli.exceptions import ScrapliAuthenticationFailed
from scrapli_transfer_utils import AsyncSrapliTransferUtils

from phantom_communicator.command_blocks.command import Command
from phantom_communicator.command_blocks.command_block import CommandBlock
from phantom_communicator.command_blocks.snmp_command import SNMPCommand
from phantom_communicator.exceptions import CommunicatorAuthenticationFailed, CommunicatorNotFound
from phantom_communicator.helpers import genie_parse

BootFiles = namedtuple("BootFiles", ["main", "backup"])


class Communicator:  # pylint: disable=R0902
    def __init__(
        self,
        host,
        username,
        password,
        os,
    ):
        self.host = host
        self.username = username
        self.password = password
        self.os = os

        self._session = None
        self._cfg_conn = None

        # channel_io is a ref to input commands, and the corresponding output
        self.channel_io = []
        self.genie_external = False

    @classmethod
    def factory(
        cls,
        host=None,
        username=None,
        password=None,
        os=None,
    ):
        return BaseCommunicator.factory(
            host=host,
            username=username,
            password=password,
            os=os,
        )

    async def genie_parse_output(self):
        """
        not sure if this one should be async
        Parse output with Cisco genie parsers, try to return structured output

        Returns:
            output: structured data

        Raises:
            N/A

        """
        genie_output = {}

        for io in self.channel_io:
            genie_output[io["command_input"]] = dict(genie_parse(self.os, io["command_input"], io["command_output"]))

        return genie_output

    async def command(self, cmd: [str, Command, SNMPCommand]):
        raise NotImplementedError

    async def send_command(self, command: str):
        raise NotImplementedError

    async def send_commands(self, commands: list):
        """
        :param commands: a list containing comands to be executed on the remote device
        :return:
        """
        raise NotImplementedError

    async def send_interactive_command(self, commands: Union[List[Tuple[str, str]], List[Tuple[str, str, bool]]]):
        raise NotImplementedError

    async def get_version(self):
        version_result = await self._cfg_conn.get_version()
        return version_result.result

    async def get_startup_config(self):
        startup_config_result = await self._cfg_conn.get_config(source="startup")
        return startup_config_result.result

    async def get_running_config(self):
        running_config_result = await self._cfg_conn.get_config(source="running")
        return running_config_result.result

    async def get_boot_files(self):
        raise NotImplementedError

    async def save_device_config(self, hostname: str):
        raise NotImplementedError

    async def file_transfer(
        self,
        operation: Literal["get", "put"],
        src: str,
        dst: str = "",
        verify: bool = True,
        device_fs: Optional[str] = None,
        overwrite: bool = False,
        force_config: bool = False,
        cleanup: bool = True,
    ):  # pylint: disable=R0913
        """
        :param operation: put/get file to/from device
        :param src: source file name
        :param dst: destination file name (same as src if omitted)
        :param verify: `True` if verification is needed (checksum, file existence, disk space)
        :param device_fs: (autodetect if empty) is not always correct in guessing tho
        :param force_config: If set to `True`, Transfer function will be enabled in device configuration
                               before transfer.
                              If set to `False`, Transfer functionality will be checked but won't
                              configure the device.
                              If set to `None`, capability won't even checked.
        :param overwrite: If set to `True`, destination will be overwritten in case hash verification
                          fails
                          If set to `False`, destination file won't be overwritten.
                          Beware: turning off `verify` will make this parameter ignored and destination
                          will be overwritten regardless! (Logic is that if user does not care about
                          checking, just copy it over)
        :param cleanup: If set to True, call the cleanup procedure to restore configuration if it was
                     altered
        :return: example: FileTransferResult(exists=True, transferred=True, verified=True)
        """
        scp = AsyncSrapliTransferUtils(self._session)
        return await scp.file_transfer(
            operation=operation,
            src=src,
            dst=dst,
            verify=verify,
            device_fs=device_fs,
            force_config=force_config,
            cleanup=cleanup,
            overwrite=overwrite,
        )

    async def __aenter__(self):
        retry = 0
        connection = False
        while not connection:
            try:
                await self._session.open()
                if self._cfg_conn:
                    await self._cfg_conn.prepare()
                connection = True

            except (ConnectionRefusedError, ConnectionLost) as e:
                retry += 1
                if retry > 10:
                    raise ConnectionLost("lost connection") from e
                await asyncio.sleep(1)

            except ScrapliAuthenticationFailed as e:
                raise CommunicatorAuthenticationFailed(
                    f"Failed to connect to {self.host} with os: {self.os} reason: {e}"
                ) from e

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()


class BaseCommunicator(Communicator):
    @classmethod
    def factory(cls, *args, **kwargs):
        from phantom_communicator.communicators.cisco_iosxe import CiscoIosXeCommunicator
        from phantom_communicator.communicators.huawei_hvrp import HuaweiVrpCommunicator

        if kwargs.get("os") == "vrp":
            return HuaweiVrpCommunicator(*args, **kwargs)
        elif kwargs.get("os") in ["ios", "iosxe"]:
            return CiscoIosXeCommunicator(*args, **kwargs)
        raise CommunicatorNotFound(f"No Communicator defined for {kwargs.get('os')}")

    def __init__(self, host, username, password, os):
        super().__init__(host, username, password, os)

    async def command(self, cmd: [str, Command, SNMPCommand]):
        cmd = getattr(self.command_block, cmd)()
        if isinstance(cmd, list):
            cmds = [x.command for x in cmd if x is not None]
            return await self.send_commands(cmds)

        elif isinstance(cmd, str):
            return await self.send_command(cmd)

        elif isinstance(cmd, SNMPCommand):
            # implement sending of SNMP commands.
            pass

        return await self.send_command(cmd.command)

        # how to handle Command??

    async def send_command(self, command: str):
        """
        :param command: command to be executed on the remote device
        note: that if you send interactive commands: ex.
        the command: copy run start on a cisco gives back a prompt:
        Destination filename [startup-config]?
        this will hang the send_command. workaround for this is to send to command with a \n seperator
        copy run start\n
        now it will be accepted. however in this example it won't help if you want to determine the dest filename
        the nicer method is to use the fuction: send_interactive_command which accepts multiple arguments
        :return:
        """
        payload = await self._session.send_command(command)
        self.channel_io.append({"command_input": command, "command_output": payload.result})
        return payload

    async def send_commands(self, commands: list):
        payloads = await self._session.send_commands(commands)
        for payload in payloads.data:
            self.channel_io.append({"command_input": payload.channel_input, "command_output": payload.result})
        return payloads

    async def send_interactive_command(self, commands: Union[List[Tuple[str, str]], List[Tuple[str, str, bool]]]):
        """
        :param commands: list of tuples containing:
        Used to interact with devices where prompts change per input, and where inputs may be hidden
        such as in the case of a password input. This can be used to respond to challenges from
        devices such as the confirmation for the command "clear logging" on IOSXE devices for
        example. You may have as many elements in the "interact_events" list as needed, and each
        element of that list should be a tuple of two or three elements. The first element is always
        the input to send as a string, the second should be the expected response as a string, and
        the optional third a bool for whether or not the input is "hidden" (i.e. password input)
        :return:
        """
        return await self._session.send_interactive(commands)
