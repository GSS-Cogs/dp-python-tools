from typing import Dict, List

from properties.base import BaseProperty
from properties.string import StringProperty
from properties.intproperty import IntegerProperty


class Config:
    @staticmethod
    def from_env(config_dict: Dict[str, Dict[str, BaseProperty]]):
        # TODO = read in and populate property classes as
        # per the example in the main readme.
        # You need to populate with dot notation in mind so:
        #
        # StringProperty("fieldname", "fieldvalue")
        #
        # should be accessed on Config/self, so:
        #
        # value = config.fieldvalue.value
        # i.e
        # config.fieldvalue = StringProperty("fieldname", "fieldvalue")
        #
        # Worth looking at the __setattr_ dunder method and a loop
        # for how to do this.
        #
        # Do track the BaseProperty's that you add ready for
        # assert_valid_config call.

        def __init__(self, config_dict):
            for key, value in config_dict.items():

                if value["class"] == StringProperty:
                    if value["kwargs"]:
                        regex = value["kwargs"].get("regex")
                        min_len = value["kwargs"].get("min_len")
                        max_len = value["kwargs"].get("max_len")
                    else:
                        regex = None
                        min_len = None
                        max_len = None

                    # Best way to determine populating regex, min len, max len
                    # if they are none?
                    stringprop = StringProperty(
                        name=value["property"],
                        value=value,
                        regex=regex,
                        min_len=min_len,
                        max_len=max_len,
                    )

                    prop_name = value["property"]

                    # Need a good design so assert_valid_config can be called
                    # on each property. Or possibly add properties to list
                    # and make assert_valid_config iterate through
                    self.assert_valid_config(stringprop)

                    setattr(self, prop_name, stringprop)

                elif value["class"] == IntegerProperty:
                    if value["kwargs"]:
                        min_val = value["kwargs"].get("min_val")
                        max_val = value["kwargs"].get("max_val")
                    else:
                        min_val = None
                        max_val = None

                    intprop = IntegerProperty(
                        name=value["property"],
                        value=value,
                        min_val=min_val,
                        max_val=max_val,
                    )

                    prop_name = value["property"]

                    self.assert_valid_config(intprop)

                    setattr(self, prop_name, intprop)

                else:
                    raise ValueError(
                        "Incorrect value type specified for property assignment."
                    )

    def assert_valid_config(self, prop: BaseProperty):
        """
        Assert that then Config class has the properties that
        provided properties.
        """
        # For each of the properties you imbided above, run
        # self.type_is_valid()
        # self.secondary_validation()
        prop.type_is_valid()
        prop.secondary_validation()
