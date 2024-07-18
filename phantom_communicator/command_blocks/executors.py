from phantom_communicator.command_blocks.command_result import CommandResult


class CommandExecutor:
    def __init__(self, communicator, command_parser):
        self.communicator = communicator
        self.command_parser = command_parser

    async def execute_command(self, cmd, cmd_obj, original_cmd_name, use_cache=True) -> list[CommandResult]:
        output = await self.communicator.command(cmd_obj, use_cache=use_cache, original_cmd_name=original_cmd_name)
        if isinstance(output, list):
            [result.apply_parser(self.command_parser) for result in output]
        else:
            output.apply_parser(self.command_parser)
        return output
