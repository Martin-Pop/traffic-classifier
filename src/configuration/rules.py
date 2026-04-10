from .core import ConfigurationRule as Rule
from common.file import get_absolute_path
from pathlib import Path

def validate_or_create_directory(path: str) -> bool:
    path_obj = Path(get_absolute_path(path))

    if path_obj.exists() and not path_obj.is_dir():
        return False

    if not path_obj.exists():
        try:
            path_obj.mkdir(parents=True, exist_ok=True)
        except Exception:
            return False

    return True


class ConfigurationRules:

    valid_directory = Rule(
        'Must be valid writable directory',
        validate_or_create_directory,
    )

    existing_file = Rule(
        'File must exist',
        lambda str_path: Path(get_absolute_path(str_path)).resolve().exists(),
    )

    is_joblib_file = Rule(
        'Must be a joblib file',
        lambda str_path: Path(get_absolute_path(str_path)).suffix == '.joblib',
    )

    positive_integer = Rule(
        'Must be a positive integer',
        lambda x: x > 0,
    )

    valid_percentage = Rule(
        'Must be between 0 and 1 inclusive',
        lambda value: 0 <= value <= 1,
    )
