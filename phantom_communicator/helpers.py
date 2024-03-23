import importlib

from phantom_communicator import logger


def genie_parse(os: str, command: str, output: str):
    try:
        Device = getattr(importlib.import_module(name=".conf.base", package="genie"), "Device")
        get_parser = getattr(importlib.import_module(name=".libs.parser.utils", package="genie"), "get_parser")
    except ModuleNotFoundError as exc:
        title = "Optional Extra Not Installed!"
        message = (
            "Optional extra 'genie' is not installed!\n"
            f"To resolve this issue, install '{exc.name}'. You can do this the following"
            " way:\n"
            "1: 'pip install -r requirements-genie.txt'\n"
        )
        logger.warning("%s - %s", title, message)
        logger.propagate = True
        return []

    genie_device = Device("scrapli_device", custom={"abstraction": {"order": ["os"]}}, os=os)

    try:
        get_parser(command, genie_device)
        genie_parsed_result = genie_device.parse(command, output=output)
        if isinstance(genie_parsed_result, (list, dict)):
            return genie_parsed_result
    except Exception as exc:  # pylint: disable=W0703
        logger.warning("failed to parse data with genie, genie raised exception: `%s`", exc)
    return []
