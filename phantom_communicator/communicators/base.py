import asyncio
from collections import defaultdict, namedtuple
from typing import List, Literal, Optional, Tuple, Union

from asyncssh import ConnectionLost
from gufo.snmp import SnmpSession
from scrapli.exceptions import ScrapliAuthenticationFailed

from phantom_communicator.command_blocks.command import Command, SNMPCommand
from phantom_communicator.command_blocks.command_result import CommandResult
from phantom_communicator.command_blocks.executors import CommandExecutor
from phantom_communicator.command_blocks.helpers import is_prefix_in_list
from phantom_communicator.exceptions import (
    CommandNotImplementedError,
    CommunicatorAuthenticationFailed,
    CommunicatorNotFound,
)
from phantom_communicator.file_transfer import FileTransferManager

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
        self.community_string = None

        self._session = None
        self._cfg_conn = None

        # channel_io is a ref to input commands, and the corresponding output
        self.channel_io = {}
        self.file_transfer_manager = None  # Initialize in __aenter__

        # SNMP Skip when failed
        self._snmp_failed = False
        self.skip_snmp_on_fail = True

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

    async def get_command_cache(self):
        return self.channel_io

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

    async def snmp_command(self, cmd: SNMPCommand):
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
        return await self.file_transfer_manager.file_transfer(
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
                self.file_transfer_manager = FileTransferManager(self._session)
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
        self.command_block = None

    async def execute_and_parse_commands(self, cmds, use_cache=False):
        return_data = []

        for cmd in cmds:
            results = await self.execute_and_parse_command(cmd, cmd, use_cache=use_cache)

            if isinstance(results, list):
                for result in results:
                    return_data.append(result)
            else:
                return_data.append(results)

        # here we group CommandResults by their command_or_parse_name because they belong together
        # ex: 2 CommandResults with command_or_parse_name "show_software" belong together
        def group_command_results_by_name(command_results):
            grouped_results = defaultdict(list)
            for result in command_results:
                grouped_results[result.command_or_parse_name].append(result)
            return dict(grouped_results)

        grouped_results = group_command_results_by_name(return_data)

        return grouped_results

    async def execute_and_parse_command(self, cmd, original_cmd_name=None, use_cache=False):
        cmd_obj = getattr(self.command_block, cmd)(type="command")()
        executor = CommandExecutor(self, self.command_block)
        return await executor.execute_command(cmd, cmd_obj, original_cmd_name=original_cmd_name, use_cache=use_cache)

    async def command(self, cmd, use_cache=False, original_cmd_name=None):
        if isinstance(cmd, list):
            async with asyncio.TaskGroup() as tg:
                results = []

                async def run_command(single_cmd):
                    result = await self.command(single_cmd, use_cache=use_cache, original_cmd_name=original_cmd_name)
                    results.append(result)

                for single_cmd in cmd:
                    tg.create_task(run_command(single_cmd))

            return results

        command_str = cmd.command if isinstance(cmd, Command) else cmd
        if not original_cmd_name:
            original_cmd_name = command_str

        if isinstance(cmd, SNMPCommand):
            # Special handling for SNMPCommand
            if self.skip_snmp_on_fail and self._snmp_failed:
                print("Skipping SNMP due to previous failure.")
                return None
            try:
                return await self.snmp_command(cmd)
            except Exception as e:
                import traceback

                traceback.print_exc()
                if "Timeout: No Response from" in str(e):
                    self._snmp_failed = True
                if not self.skip_snmp_on_fail:
                    raise
            return None

        # For Command or string types, send the command
        try:
            return await self.send_command(command_str, original_cmd_name=original_cmd_name, use_cache=use_cache)
        except CommandNotImplementedError:
            return "Command not implemented."

        # Fallback for unrecognized command types
        return "Unrecognized command type."

    # async def command(self, cmd, use_cache=False, original_cmd_name=None):
    #     if isinstance(cmd, list):
    #         # Handle a list of commands
    #         results = []
    #         for single_cmd in cmd:
    #             result = await self.command(single_cmd, use_cache=use_cache, original_cmd_name=original_cmd_name)
    #             results.append(result)
    #         return results
    #
    #     if isinstance(cmd, str) or isinstance(cmd, Command):
    #         # Handle string and Command instances
    #         try:
    #             if not original_cmd_name:
    #                 original_cmd_name = cmd or cmd.command
    #             return await self.send_command(cmd.command, original_cmd_name=original_cmd_name, use_cache=use_cache)
    #         except CommandNotImplementedError:
    #             pass
    #         return await self.send_command(
    #             cmd.command,
    #             original_cmd_name=original_cmd_name if isinstance(cmd, Command) else cmd,
    #             use_cache=use_cache,
    #         )
    #
    #     elif isinstance(cmd, SNMPCommand):
    #         # If this is an SNMPCommand, do the snmp readout and return the output
    #         if self.skip_snmp_on_fail and self._snmp_failed:
    #             print("Skipping snmp because of previous failure")
    #         else:
    #             try:
    #                 return await self.snmp_command(cmd)
    #             except Exception as e:
    #                 import traceback
    #
    #                 traceback.print_exc()
    #                 if "Timeout: No Response from" in str(e):
    #                     self._snmp_failed = True
    #                 if not self.skip_snmp_on_fail:
    #                     raise
    #         return None
    #
    #     # Fallback for unrecognized command types
    #     return "Unrecognized command type"

    async def send_command(self, command: str, original_cmd_name=None, use_cache=True):
        """
        Sends a command to the remote device and returns the result.

        If caching is enabled and the command result is already cached, the cached result is returned.
        For interactive commands, consider using `send_interactive_command` instead.

        note: that if you send interactive commands:
        ex. the command: copy run start on a cisco gives back a prompt: Destination filename [startup-config]?
        this will hang the send_command.
        workaround for this is to send to command with a \n seperator copy run start\n now it will be accepted.
        however in this example it won't help if you want to determine the dest filename.
        The nicer method is to use the function: send_interactive_command which accepts multiple arguments

        :param command: The command to be executed on the remote device.
        :param original_cmd_name: The original name of the command, used for logging or referencing.
        :param use_cache: Whether to use the cached result if available.
        :return: A CommandResult object containing the command result.
        """
        if use_cache:
            cached_output = self.channel_io.get(command)
            if cached_output:
                return CommandResult(
                    command_name=command,
                    raw_result=cached_output["raw_result"],
                    result=cached_output["result"],
                    command_or_parse_name=original_cmd_name or command,
                    cmd_type="str",
                )

        payload = await self._session.send_command(command)
        if use_cache:
            self.channel_io[command] = {"raw_result": payload.raw_result, "result": payload.result}

        return CommandResult(
            command_name=command,
            raw_result=payload.raw_result,
            result=payload.result,
            command_or_parse_name=original_cmd_name or command,
            cmd_type="str",
        )

    async def send_commands(self, commands: list, use_cache=False):
        payloads = await self._session.send_commands(commands)
        for payload in payloads.data:
            if use_cache:
                self.channel_io[payload.channel_input] = {
                    "raw_result": payload.raw_result,
                    "result": payload.result,
                }
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

    async def create_snmp_session(self, cmd: SNMPCommand):
        cmd.agent = cmd.agent or self.host
        cmd.community_string = cmd.community_string or self.community_string
        return SnmpSession(addr=cmd.agent, community=cmd.community_string, timeout=5.0, limit_rps=10)

    async def snmp_command(self, cmd: SNMPCommand):
        try:
            async with await self.create_snmp_session(cmd) as snmp_session:
                if cmd.type == "get":
                    snmp_output = await snmp_session.get(cmd.oid)
                    result = snmp_output.decode("utf-8") if isinstance(snmp_output, bytes) else snmp_output
                    return CommandResult(
                        command_name=cmd.command,
                        raw_result=snmp_output,
                        result=result,
                        command_or_parse_name=cmd.command,
                        cmd_type="snmp",
                    )
                elif cmd.type == "bulk":
                    snmp_output = await self.process_bulk_snmp(snmp_session, cmd)
                    return CommandResult(
                        command_name=cmd.command,
                        raw_result=None,
                        result=snmp_output,
                        command_or_parse_name=cmd.command,
                        cmd_type="snmp",
                    )
        except TimeoutError:
            return CommandResult(
                command_name=cmd.command,
                raw_result="Timeout",
                result="Timeout",
                command_or_parse_name=cmd.command,
                cmd_type="snmp",
            )
        except Exception as e:
            return CommandResult(
                command_name=cmd.command,
                raw_result=str(e),
                result="Error",
                command_or_parse_name=cmd.command,
                cmd_type="snmp",
            )

    async def process_bulk_snmp(self, snmp_session, cmd: SNMPCommand):
        results = []
        async for oid, value in snmp_session.getbulk(cmd.oid):
            if not cmd.valid_mib_prefixes or is_prefix_in_list(oid, cmd.valid_mib_prefixes):
                decoded_value = value.decode("utf-8") if isinstance(value, bytes) else value
                results.append((oid, decoded_value))
        return results
