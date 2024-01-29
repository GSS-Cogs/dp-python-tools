import pytest

from config import Config
from properties.string import StringProperty
from properties.intproperty import IntegerProperty

# def test_config_loader():

#     config_dictionary = {
#     "SOME_STRING_ENV_VAR": {
#         "class": StringProperty,
#         "property": "name1",
#         "kwargs": {
#             "regex": "I match a thing",
#             "min_len": 10
#         },
#     },
#     "SOME_URL_ENV_VAR": {
#         "class": StringProperty,
#         "property": "name2",
#         "kwargs": {
#             "regex": "https://.*"
#         },
#     },
#     "SOME_INT_ENV_VAR": {
#         "class": IntegerProperty,
#         "property": "name3",
#         "kwargs": {
#             "min_value": 5,
#             "max_value": 27
#         }
#     },
# }

#     config = Config.from_env(config_dictionary)
#     pass


config_dictionary = {
    "SOME_STRING_ENV_VAR": {
        "class": StringProperty,
        "property": "name1",
        "kwargs": {
            "regex": "I match a thing",
            "min_len": 10
        },
    },
    "SOME_URL_ENV_VAR": {
        "class": StringProperty,
        "property": "name2",
        "kwargs": {
            "regex": "https://.*"
        },
    },
    "SOME_INT_ENV_VAR": {
        "class": IntegerProperty,
        "property": "name3",
        "kwargs": {
            "min_value": 5,
            "max_value": 27
        }
    },
}

x = 3