import json
from pathlib import Path
from typing import Dict, Optional, Union
from urllib.parse import urlparse

import jsonschema
from jsonschema import ValidationError

"""
# data_dict is for passing in a dictionary to be validated
validate_json_schema("/path/to/schema.json", data_dict=some_dictionary)

# msg is to include a helpful context when debugging (i.e "what we're validating")
validate_json_schema("/path/to/schema.json", data_dict=some_dictionary, msg="Some helpful message should this validation fail")

validate_json_schema("/path/to/schema.json", data_path="/path/to/some/json", msg="Some helpful message should this validation fail")

# indent should pretty print the json contents of the error to make it
# more easily parsed by humans
validate_json_schema("/path/to/schema.json", data_dict=some_dictionary, indent=2)
"""


def validate_json_schema(
    schema_path: str,
    data_dict_or_path: Union[Dict, str],
    msg: str = "",
    indent: int = 2,
) -> Optional[ValidationError]:
    """
    Validate metadata.json files against schema provided.

    `schema_path`: file path of schema to validate against
    `data_dict_or_path`: file path or dictionary of data to be validated
    `msg`: optional string to provide additional information about validation
    `indent`: optional integer to be used when indenting json output
    """
    # Load schema as dict
    parsed_schema_path = urlparse(schema_path)
    if parsed_schema_path.scheme == "http":
        # TODO Load schema from URL
        raise NotImplementedError("Validation from remote schema not yet supported")
    else:
        with open(Path(schema_path), "r") as f:
            schema_from_path = json.load(f)

    # Load data as dict
    if isinstance(data_dict_or_path, Dict):
        data_to_validate = data_dict_or_path
    elif isinstance(data_dict_or_path, str):
        with open(Path(data_dict_or_path), "r") as f:
            data_to_validate = json.load(f)
    else:
        raise ValueError("Invalid data format")

    # Validate data against schema
    print(msg)
    try:
        jsonschema.validate(data_to_validate, schema_from_path)
    except jsonschema.ValidationError as err:
        # TODO Handle jsonschema.SchemaError?
        print(f"Error when validating data: {err.message}")
        # If the error relates to a specific field, print the error's location
        if err.json_path != "$":
            print(f"Error in data field: {err.json_path}")
        # Print the data that failed validation
        print(f"Contents of data:\n{json.dumps(data_to_validate, indent=indent)}")
        return err
