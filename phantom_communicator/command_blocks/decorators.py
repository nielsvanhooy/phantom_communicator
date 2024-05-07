from functools import wraps

from phantom_communicator.command_blocks.command import Command
from phantom_communicator.command_blocks.command_block import CommandBlock
from phantom_communicator.command_blocks.helpers import commands_list


class command:
    def __init__(self, name=None, vendor=None, model=None, os=None):
        self.name = name
        self.vendor = vendor
        self.model = [model] if type(model) in [str, type(None)] else model
        self.os = os

    def register(self, model, method):
        model = model.upper() if model else None
        CommandBlock.register_command(self.name, self.vendor, model, self.os, method)

    def __call__(self, method):
        for model in self.model:
            self.register(model, method)
        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        return wrapper


def return_config(vendor=None, end=False, custom=False):
    """
    Create a list of Command's and append end/quit if 'end' is True

    :param vendor:
    :param end:
    :param custom:
    :return:
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)

            if not result:
                return []

            if end:
                if vendor == "cisco":
                    if custom:
                        result.append(Command(" exit"))
                    else:
                        result.append(" exit")
                elif vendor == "huawei":
                    result.append(" quit")
            if custom:
                return result
            else:
                return commands_list(result)

        return wrapper

    return decorator