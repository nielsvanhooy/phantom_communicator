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