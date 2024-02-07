from pathlib import Path

import pytest
from dpytools.validation.json.validation import validate_json_schema


def test_validate_json_schema_data_path():
    """
    Validate data (as file path) against schema
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = "tests/test_cases/pipeline_config.json"
    assert (
        validate_json_schema(
            pipeline_config_schema,
            pipeline_config,
            "Validating pipeline_config.json",
        )
        is None
    )


def test_validate_json_schema_data_dict():
    """
    Validate data (as dictionary) against schema
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = {
        "schema": "airflow.schemas.ingress.sdmx.v1.schema.json",
        "required_files": [{"matches": "*.sdmx", "count": 1}],
        "supplementary_distributions": [{"matches": "*.sdmx", "count": 1}],
        "priority": 1,
        "contact": ["jobloggs@ons.gov.uk"],
        "pipeline": "default",
    }
    assert (
        validate_json_schema(
            pipeline_config_schema,
            pipeline_config,
            "Validating pipeline_config dict",
        )
        is None
    )


def test_validate_json_schema_invalid_data_format():
    """
    Raise ValueError if data is not a file path or dictionary
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = ["Invalid", "data", "format"]
    with pytest.raises(ValueError):
        validate_json_schema(pipeline_config_schema, pipeline_config)


def test_validate_json_schema_url():
    """
    Raise NotImplementedError if schema path is a URL (i.e. not a local file)
    """
    pipeline_config_schema = "http://example.org"
    pipeline_config = "tests/test_cases/pipeline_config.json"
    with pytest.raises(NotImplementedError):
        validate_json_schema(pipeline_config_schema, pipeline_config)


def test_validate_json_schema_data_path_required_field_missing():
    """
    Raises ValidationError due to missing field in data (as file path) being validated
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = "tests/test_cases/pipeline_config_missing_required_field.json"
    err = validate_json_schema(
        pipeline_config_schema,
        pipeline_config,
        "Validating pipeline_config_missing_required_field.json",
    )
    assert err.message == "'priority' is a required property"


def test_validate_json_schema_data_path_invalid_data_type():
    """
    Raises ValidationError due to invalid data type in data (as file path) being validated
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = "tests/test_cases/pipeline_config_invalid_data_type.json"
    err = validate_json_schema(
        pipeline_config_schema,
        pipeline_config,
        "Validating pipeline_config_invalid_data_type.json",
    )
    assert err.message == "'1' is not of type 'integer'"


def test_validate_json_schema_data_dict_required_field_missing():
    """
    Raises ValidationError due to missing field in data (as dictionary) being validated
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = {
        "schema": "airflow.schemas.ingress.sdmx.v1.schema.json",
        "required_files": [{"matches": "*.sdmx", "count": 1}],
        "supplementary_distributions": [{"matches": "*.sdmx", "count": 1}],
        "contact": ["jobloggs@ons.gov.uk"],
        "pipeline": "default",
    }
    err = validate_json_schema(
        pipeline_config_schema,
        pipeline_config,
        "Validating pipeline_config with required field missing",
    )
    assert err.message == "'priority' is a required property"


def test_validate_json_schema_data_dict_invalid_data_type():
    """
    Raises ValidationError due to invalid data type in data (as dictionary) being validated
    """
    pipeline_config_schema = "tests/test_cases/pipeline_config_schema.json"
    pipeline_config = {
        "schema": "airflow.schemas.ingress.sdmx.v1.schema.json",
        "required_files": [{"matches": "*.sdmx", "count": 1}],
        "supplementary_distributions": [{"matches": "*.sdmx", "count": "1"}],
        "priority": 1,
        "contact": ["jobloggs@ons.gov.uk"],
        "pipeline": "default",
    }
    err = validate_json_schema(
        pipeline_config_schema,
        pipeline_config,
        f"Validating pipeline_config dict with invalid data type",
    )
    assert err.message == "'1' is not of type 'integer'"
