from typing import Dict


# Mapping of strings to bools for str_to_bool function to work
valid_bool_values: Dict[str, bool] = {
    "true": True,
    "1": True,
    "false": False,
    "0": False,
}


def str_to_bool(str_val: str, default: bool = False) -> bool:
    """Convert input strings to the correct boolean format in order to set environment variable value"""
    return valid_bool_values.get(str_val.lower(), default)
