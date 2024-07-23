import re


def get_config_item(config: str, item: str, global_command: bool = True, wildcard: bool = False) -> bool:
    """
    config:     full_config or partial config
    item:       searchstring
    start:      boolean from start = default
    wildcard:   boolean (search complete item no values behind)
                like router bgp xxx
                -> get_config_item('router bgp', wildcard=True)

    return Boolean True if item is found
    """
    if wildcard:
        item += " "

    if global_command:
        results = re.findall(f"^{item}", config, re.MULTILINE)
    else:
        results = re.findall(f"{item}", config, re.MULTILINE)
    return True if results else False
