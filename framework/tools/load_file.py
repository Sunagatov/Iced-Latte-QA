import os
import json

import os
import json


def load_file_json(directory, file_name, file_type='json'):
    """
    Load content from a file located in the specified directory.

    Args:
        directory (str): The directory where the file is located.
        file_name (str): The name of the file to load.
        file_type (str): The type of file, which dictates how the content is loaded.

    Returns:
        The content of the file, parsed according to the file_type argument.
    """
    # Construct the absolute file path
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), directory, file_name)
    print(f"Loading file from: {file_path}")  # Debugging print
    # Load and return the file content based on its type
    if file_type == 'json':
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Failed to load or parse the JSON file {file_path}. Error: {e}")
            return []
    else:
        print(f"Unsupported file type: {file_type}")
        return []
