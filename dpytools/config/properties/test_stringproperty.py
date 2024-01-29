import pytest
from properties import StringProperty

def test_string_property():
    """
    Tests if a string property instance can be created 
    and validated with no errors.
    """

    test_property = StringProperty(
        name = "Test String Property",
        value = "Test string value",
        regex = "Test regex",
        min_len = 1,
        max_len = 40
    )

    test_property.secondary_validation_passed()


def test_string_property_empty_val():
    """
    Tests if a string property with an empty string as the value
    raises the expected exception from the secondary validation.
    """

    test_property = StringProperty(
        name = "Test String Property",
        value = "",
        regex = "Test regex",
        min_len = 1,
        max_len = 40
    )

    with pytest.raises(ValueError) as e:

        test_property.secondary_validation_passed()

        assert (
            f"Str value for Test String Property is an empty string") in str(e.value)


def test_string_property_min_len():
    """
    Tests if a string property instance with a non-matching minimum 
    length string raises the expected error from secondary validation.
    """

    test_property = StringProperty(
        name = "Test String Property",
        value = "Test string value",
        regex = "Test regex",
        min_len = 50,
        max_len = 51
    )

    with pytest.raises(ValueError) as e:

        test_property.secondary_validation_passed()

        assert "Str value for Test String Property is shorter than minimum length 50" in str(e.value)


def test_string_property_max_len():
    """
    Tests if a string property instance with a non-matching maximum 
    length string raises the expected error from secondary validation.
    """

    test_property = StringProperty(
        name = "Test String Property",
        value = "Test string value",
        regex = "Test regex",
        min_len = 1,
        max_len = 2
    )

    with pytest.raises(ValueError) as e:

        test_property.secondary_validation_passed()

        assert (
            "Str value for Test String Property is longer than maximum length 2") in str(e.value)