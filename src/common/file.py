import sys
import os

def get_resource_path(relative_path):
    """
    Gets absolute path based on execution.
    Works for local execution and for PyInstaller.
    :param relative_path: relative path to resolve
    """
    try:
        # pyinstallers temp path is stored in sys._MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)