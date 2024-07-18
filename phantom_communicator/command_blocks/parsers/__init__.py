import importlib
import os
import pkgutil


def import_submodules_from_folders(base_package, subfolders):
    """
    Dynamically imports all modules from specified subfolders within a base package.

    :param base_package: The base package name as a string.
    :param subfolders: A list of subfolder names within the base package.
    """
    base_path = os.path.dirname(__file__)  # Adjust this based on the file's location relative to the project root

    for subfolder in subfolders:
        package_dir = os.path.join(base_path, subfolder)
        package_name = f"{base_package}.{subfolder}"

        for finder, name, ispkg in pkgutil.iter_modules([package_dir]):
            module_name = f"{package_name}.{name}"
            importlib.import_module(module_name)


base_package = "phantom_communicator.command_blocks.parsers"
subfolders = ["iosxe", "hvrp"]
importing = import_submodules_from_folders(base_package, subfolders)
