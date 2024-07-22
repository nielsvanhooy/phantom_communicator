from functools import wraps
from typing import Callable

from phantom_communicator.command_blocks.command import Command
from phantom_communicator.command_blocks.command_and_parse import CommandParser
from phantom_communicator.command_blocks.helpers import commands_list


class command_or_parse:
    def __init__(self, name=None, vendor=None, model=None, os=None, type="command"):
        self.name = name
        self.vendor = vendor
        self.model = [model] if isinstance(model, str) or model is None else model
        self.os = os
        self.type = type

    def register(self, model, method):
        model = model.upper() if model else None
        if self.type == "command":
            CommandParser.register_command(self.name, self.vendor, model, self.os, method)
        elif self.type == "parse_command":
            CommandParser.register_parse_command(self.name, self.vendor, model, self.os, method)

    def __call__(self, method):
        for model in self.model:
            self.register(model, method)

        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)

        return wrapper


def return_config(vendor: str = None, end: bool = False, custom: bool = False) -> Callable:
    """
    Create a list of Command's and append end/quit if 'end' is True

    :param vendor: The vendor name
    :param end: Whether to append an exit command
    :param custom: Whether the result is custom or should be converted
    :return: Decorated function
    """
    vendor_exit_commands = {
        "cisco": " exit",
        "huawei": " quit",
    }

    def decorator(f: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> list:
            result = f(*args, **kwargs)

            if not result:
                return []

            exit_command = vendor_exit_commands.get(vendor)
            if end and exit_command:
                result.append(Command(exit_command) if custom else exit_command)

            return result if custom else commands_list(result)

        return wrapper

    return decorator
