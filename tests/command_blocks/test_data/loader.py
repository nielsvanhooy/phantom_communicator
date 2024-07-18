def load_test_data(test_data_name):
    """
    Load test data from a JSON file located in the 'tests/fixtures' directory.
    The file name should match the test_data_name argument and have a '.json' extension.

    :param test_data_name: The name of the test data file (without extension)
    :return: The content of the test data file as a string
    """
    file_path = f"test_data/{test_data_name}.txt"
    with open(file_path, "r") as file:
        data = file.read()
    return data
