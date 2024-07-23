import re


def get_config_value_position(config: str, item: str, position: int = 0, global_command: bool = True) -> list:
    """
    config:    full_config
    item:      searchstring
    idx:       index value to return

    return Value[index] if line starts with item in full config
    """
    return_results = []

    if global_command:
        results = re.findall(f"^{item} (.*)", config, re.MULTILINE)
    else:
        results = re.findall(f"{item} (.*)", config, re.MULTILINE)

    for result in results:
        items = result.split(" ")
        try:
            return_results.append(items[position])
        except IndexError:
            continue

    return return_results
