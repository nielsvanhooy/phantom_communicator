from dataclasses import dataclass, field
from typing import Optional, Union

from phantom_communicator.exceptions import CommandNotImplementedError

# dataclass test


@dataclass
class CommandResult:
    command_name: str
    raw_result: Optional[str] = None
    result: Union[str, list] = field(default_factory=list)
    structured_data: Optional[dict] = None
    parsed_output: Optional[str] = None
    command_or_parse_name: Optional[str] = None
    cmd_type: Optional[str] = None

    def apply_parser(self, command_parser):
        try:
            parser_function = command_parser.get_specific_command(self.command_or_parse_name, type="parse_command")
            if parser_function:
                self.parsed_output = parser_function(self)
            else:
                self.parsed_output = "Parser function not found"
        except CommandNotImplementedError:
            self.parsed_output = "Parser function not implemented"

    def __repr__(self) -> str:
        return f"CommandResult(command_name={self.command_name!r}, cmd_type={self.cmd_type!r}, command_or_parse_name={self.command_or_parse_name!r}, parsed_output={self.parsed_output!r}, result={self.result!r}, structured_data={self.structured_data!r})"


#
# class CommandResult:
#     def __init__(
#         self,
#         command_name: str,
#         raw_result: str | None,
#         result: str | list,
#         structured_data=None,
#         parsed_output=None,
#         command_or_parse_name=None,
#         cmd_type=None,
#     ):
#         self.command_name = command_name
#         self.raw_result = raw_result
#         self.result = result
#         self.structured_data = structured_data
#         self.parsed_output = parsed_output
#         self.command_or_parse_name = command_or_parse_name
#         self.cmd_type = cmd_type
#
#     def apply_parser(self, command_parser):
#         try:
#             parser_function = command_parser.get_specific_command(self.command_or_parse_name, type="parse_command")
#             if parser_function:
#                 self.parsed_output = parser_function(self)
#             else:
#                 self.parsed_output = "Parser function not found"
#         except CommandNotImplementedError:
#             self.parsed_output = "Parser function not implemented"
#
#     def __repr__(self) -> str:
#         return f"CommandResult({self.command_name=} {self.cmd_type=})"
