import json
from dpytools.logger.logger import DpLogger
import pytest
import structlog
from structlog.testing import LogCapture
import jsonschema

# TODO Add tests for http and auth fields


# TODO Figure out how to move fixtures to tests.fixtures.log_output.py
@pytest.fixture(name="log_output")
def fixture_log_output():
    return LogCapture()


@pytest.fixture(autouse=True)
def fixture_configure_structlog(log_output):
    structlog.configure(processors=[log_output])


# Create logger
# test_mode=True returns the dictionary being logged from the logging statement.
logger = DpLogger("test-1", test_mode=True)


def do_something(level: str):
    if level == "debug":
        logger.debug("Debug")
    elif level == "arbitrary":
        logger.debug("Debug", data={"arbitrary_key": "arbitrary_value"})
    elif level == "raw":
        logger.debug("Debug", raw="raw")
    elif level == "info":
        logger.info("Info")
    elif level == "warning":
        logger.warning("Warning")
    elif level == "error":
        logger.error("Error", ValueError)
    elif level == "critical":
        logger.critical("Critical", ValueError)


# Schemas to validate log entries against
# Created with https://www.liquid-technologies.com/online-json-to-schema-converter
with open("tests/test_cases/logging_schema.json", "r") as fp:
    schema = json.load(fp)

with open("tests/test_cases/logging_schema_with_error.json", "r") as fp:
    schema_with_error = json.load(fp)


def test_debug_no_arbitrary_data(log_output):
    """
    Test that we get the expected structure when constructing
    a debug log.
    """
    do_something("debug")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema) is None


def test_info_no_arbitrary_data(log_output):
    """
    Test that we get the expected structure when constructing
    an info log.
    """
    do_something("info")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema) is None


def test_warning_no_arbitrary_data(log_output):
    """
    Test that we get the expected structure when constructing
    a warning log.
    """
    do_something("warning")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema) is None


def test_error_no_arbitrary_data(log_output):
    """
    Test that we get the expected structure when constructing
    an error log.
    """
    do_something("error")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema_with_error) is None


def test_critical_no_arbitrary_data(log_output):
    """
    Test that we get the expected structure when constructing
    a critical log.
    """
    do_something("critical")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema_with_error) is None


def test_debug_with_arbitrary_data(log_output):
    """
    Test that we get the expected structure when constructing
    a debug log with arbitrary data.
    """
    do_something("arbitrary")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema) is None


def test_debug_with_raw_data(log_output):
    """
    Test that we get the expected structure when constructing
    a debug log with raw data.
    """
    do_something("raw")
    output_dict = log_output.entries[0]
    # Validate output_dict against schema
    assert jsonschema.validate(instance=output_dict, schema=schema) is None
