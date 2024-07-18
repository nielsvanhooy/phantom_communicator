from phantom_communicator.exceptions import CommandNotImplementedError


class CommandParser:
    commands = {}
    parsers = {}

    def __init__(self, vendor=None, model=None, os=None):
        from phantom_communicator.command_blocks import commands  # noqa
        from phantom_communicator.command_blocks import parsers  # noqa

        self.vendor = vendor
        self.model = model.upper() if model else None
        self.os = os

    @classmethod
    def factory(cls, vendor=None, model=None, os=None):
        return cls(vendor=vendor, model=model, os=os)

    @classmethod
    def register_command(cls, command_name, vendor, model, os, method):
        vendor_cmds = cls.commands.setdefault(vendor, {})
        os_cmds = vendor_cmds.setdefault(model, {})
        cmds = os_cmds.setdefault(os, {})
        cmds[command_name] = method

    @classmethod
    def register_parse_command(cls, command_name, vendor, model, os, method):
        vendor_cmds = cls.parsers.setdefault(vendor, {})
        os_cmds = vendor_cmds.setdefault(model, {})
        cmds = os_cmds.setdefault(os, {})
        cmds[command_name] = method

    def get_specific_command(self, command, type="command"):
        if type == "command":
            vendor_cmds = self.commands.get(self.vendor, {})
        else:  # Assuming type == 'parse_command'
            vendor_cmds = self.parsers.get(self.vendor, {})

        os_cmds = vendor_cmds.get(self.model, {})
        cmds = os_cmds.get(self.os, {})
        cmd = cmds.get(command)

        if cmd is None and self.os == "ios":
            cmd = cmds.get("iosxe", {}).get(command)

        if cmd is None:
            raise CommandNotImplementedError(
                f"Command or parse command '{command}' not implemented for {self.vendor}, {self.model}, {self.os}"
            )

        return cmd

    def __getattr__(self, item):
        def command_function(**kwargs):
            type = kwargs.get("type", "command")
            return self.get_specific_command(item, type)

        return command_function
