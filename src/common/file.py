import json
import sys
import os

def get_absolute_path(relative_path):
    """
    Gets absolute path based on execution.
    Works for local execution and for PyInstaller.
    :param relative_path: relative path to resolve
    """

    if os.path.isabs(relative_path):
        return relative_path

    try:
        # pyinstallers temp path is stored in sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("..") # depends on where main is!!!

    return os.path.join(base_path, relative_path)

def try_load_json_from_file(file_path):
    try:
        with open(file_path, "r") as json_file:
            return json.load(json_file), None
    except Exception as e:
        return None, str(e)
