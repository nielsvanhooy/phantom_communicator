class Command:
    """
    Direct command to be executed on the CPE
    """

    __slots__ = ["command", "timeout", "expected_prompt", "error_condition"]
    forbidden = ["write erase", "reset saved-configuration", "wr era",
                 "delete startup-config", "delete running-config", "configure replace"]

    def __init__(self, command, timeout=10, skip_forbidden=False):
        self.command = command if skip_forbidden or not any(
            x for x in self.forbidden if x in command.strip().lower()
        ) else ""
        self.timeout = timeout

    def __str__(self) -> str:
        return self.command

    def __dict__(self) -> dict:
        return {
            "command": self.command,
            "timeout": self.timeout,
        }

    def __eq__(self, other):
        return self.__dict__() == other.__dict__()

    def __repr__(self) -> str:
        return f"<Command {self.__dict__()}>"


class Parse(Command):
    def __init__(self, command, timeout=10):
        super().__init__(command, timeout=10)


class CommandConstructor:
    """
    CommandConstructor is used for determining whether a command should be
    executed within its context. This can be useful for for instance show
    commands in the Meta process, where a command is always part of the show
    flow but should only execute if the CPE has WAN ports of type "lte"

    Should return an instance or a list of instances of <Command>
    """

    def is_eligible_to_execute(self, *args, **kwargs):
        raise NotImplementedError

    def get_commands(self, *args, **kwargs) -> list[Command]:
        raise NotImplementedError