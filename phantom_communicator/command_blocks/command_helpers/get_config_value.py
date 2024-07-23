import re


def get_config_value(
    config: str,
    item: str,
    return_list: bool = False,
    global_command: bool = True,
    whitespace: bool = True,
    lower: bool = False,
) -> object:
    """
    config:      full_config
    item:        searchstring
    return_list: boolean

    return all Values behind item. if line starts with item in full config
    line can start with indent
    if return_list = True return list of ALL config_line values else only
    first item

    example:
    ip helper-address 1.1.1.1
    ip helper-address 2.2.2.2

    get_config_value(config, 'ip helper-address') --> 1.1.1.1
    get_config_value(config, 'ip helper-address', True) --> [1.1.1.1, 2.2.2.2]
    """
    if lower:
        config = config.lower()

    whitespace = " " if whitespace else ""

    if global_command:
        results = re.findall(f"^{item}{whitespace}(.*)", config, re.MULTILINE)
    else:
        results = re.findall(rf"^\s+{item}{whitespace}(.*)", config, re.MULTILINE)  # noqa: W605,E501

    if return_list:
        return results if len(results) > 0 else None

    return results[0] if len(results) > 0 else None
