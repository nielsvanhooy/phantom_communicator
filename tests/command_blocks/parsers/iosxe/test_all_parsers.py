import pytest
import re
import importlib.util
from phantom_communicator.command_blocks.command_result import CommandResult
from pathlib import Path

# Define a mapping between test file base names and parsing function names
# if fixture files ex: 001.txt (has just text), 002.txt (has python object) mixed type of input = use "python"
# otherwise use "str"
parsing_function_mapping = {
    "show_config_dhcp": ("iosxe", "parse_show_run_dhcp", "str"),
    "show_inventory": ("iosxe", "parse_show_inventory", "python"),
    "show_software": ("iosxe", "parse_show_software", "python"),
    "show_version": ("iosxe", "parse_show_ver", "str")
    # Add more mappings as needed
}


def load_fixture(fixture_path):
    with open(fixture_path, "r") as file:
        return file.read()


def discover_fixture_files():
    test_file_dir = Path(__file__).parent
    fixture_dir = test_file_dir / "fixtures"
    pattern = re.compile(r"^\d{3}\.txt$")

    # Extract keys from parsing_function_mapping and prepend 'test_' to match directory names
    valid_directories = ["test_" + key for key in parsing_function_mapping.keys()]

    # Discover fixture files only in directories that match keys in parsing_function_mapping
    fixtures = []
    for f in fixture_dir.rglob("*.txt"):
        if pattern.match(f.name):
            parent_dir_name = f.parent.name
            if parent_dir_name in valid_directories:
                fixtures.append(str(f))

    return fixtures


def import_expected_results(result_file_path):
    spec = importlib.util.spec_from_file_location("expected_results", result_file_path)
    expected_results = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(expected_results)
    return expected_results.expected_results


def call_parsing_function(function_name, os, command_results, test_file_base_name):
    # Dynamically construct the module path based on the test file base name
    module_path = f"phantom_communicator.command_blocks.parsers.{os}.{test_file_base_name}"
    module = __import__(module_path, fromlist=[function_name])
    parsing_function = getattr(module, function_name)
    return parsing_function(command_results)


@pytest.mark.parametrize("fixture_file", discover_fixture_files())
def test_parse_dhcp_config(fixture_file):
    # Convert fixture_file string to Path object for easier manipulation
    fixture_path = Path(fixture_file)
    # Dynamically extract the directory name and prune the prefix
    test_case_name = fixture_path.parent.name.removeprefix("test_")

    fixture_content = load_fixture(fixture_file)

    # Use test_case_name to dynamically determine the parsing function
    # Assuming test_case_name matches keys in parsing_function_mapping after processing
    function_name_tuple = parsing_function_mapping.get(test_case_name)
    if not function_name_tuple:
        raise ValueError(f"No parsing function found for {test_case_name}")
    function_name = function_name_tuple[1]
    os = function_name_tuple[0]

    command_results = CommandResult("", cmd_type="str", result=fixture_content)
    if function_name_tuple[2] == "python":
        try:
            fixture_content = eval(fixture_content)
            command_results = CommandResult("", cmd_type=fixture_content["cmd_type"], result=fixture_content["result"])
        except SyntaxError:
            pass

    # Dynamically call the parsing function
    result = call_parsing_function(function_name, os, command_results, test_case_name)

    # Construct the path to the corresponding result file
    result_file_name = "result_" + fixture_path.stem + ".py"
    result_file_path = fixture_path.parent / result_file_name

    expected_results = import_expected_results(str(result_file_path))

    # Perform detailed assertions comparing result with expected_results
    assert result == expected_results, f"Result does not match expected results for {fixture_file}"
