from phantom_communicator.exceptions import CommandNotImplementedError


class CommandBlock:
    commands = {}

    def __init__(self, vendor=None, model=None, os=None):
        from phantom_communicator.command_blocks import commands  # noqa: F401
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

    def get_specific_command(self, command):
        vendor_cmds = self.commands.get(self.vendor, {})
        os_cmds = vendor_cmds.get(self.model, {})
        cmds = os_cmds.get(self.os, {})

        cmd = cmds.get(command)

        if cmd is None and self.os == "ios":
            # If command is not found and os is 'ios', try with os as 'iosxe'
            cmd = cmds.get("iosxe", {}).get(command)

        if cmd is None:
            # If command not found, raise CommandNotImplementedError
            raise CommandNotImplementedError

        return cmd

    def __getattr__(self, item):
        try:
            return self.get_specific_command(item)
        except CommandNotImplementedError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")