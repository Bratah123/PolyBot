"""YAML Parser

Intentionally avoiding the use of classes in favour of top-level functions.
See the parser docs here:
https://yaml.readthedocs.io/en/latest/index.html
"""
from ruamel.yaml import YAML


print("  [DEBUG] Attempting to load YAML files")
# Create YAML parser object
yaml = YAML(typ="safe", pure=True)


# Design choice: Have the bot read the YAML contents into memory,
#   and then hold it in memory, because when the player base is large,
#   player commands can be quite frequent. It would not be ideal for the bot
#   to need to perform expensive IO operations too often.

def yaml_load(filepath) -> "Reads the contents of a single-document YAML file":
    """
    Uses the load() function from the ruamel.yaml library to read the contexts
    of a single-document YAML file, and close it after reading.
    Note that currently, only UTF-8 and UTF-16 are supported.

    Args:
        filepath: path to the YAML file

    Returns:
        data: contents of the YAML file

    Raises:
        Generic error
    """
    try:
        with open(filepath, "r") as file_data:
            data = yaml.load(file_data)
    # In case of OS error from invalid file/path
    except Exception as e:
        print(
            "Error! The following exception was encountered while"
            f"trying to read a YAML file:\n  {e}"
        )
    return data
