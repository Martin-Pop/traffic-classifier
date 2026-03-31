import json
import sys
import os
import hashlib

def get_absolute_path(relative_path):
    """
    Returns the absolute path corresponding to a given relative path,
    resolving it relative to the project root.

    The function works for:
    Scripts executed directly
    PyInstaller-packaged executables

    If the given path is already absolute, it is returned unchanged.
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


def calculate_file_hash(filepath, chunk_size=65536):
    hasher = hashlib.sha256()

    with open(filepath, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(chunk_size)

    return hasher.hexdigest()