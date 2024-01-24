from typing import Dict

from .properties.base import BaseProperty

class Config:

    @staticmethod
    def from_env(config_dict: Dict[str, BaseProperty]):
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
        ...

    def assert_valid_config(self):
        """
        Assert that then Config class has the properties that
        provided properties.
        """

        # For each of the properties you imbided above, run
        # self.type_is_valid()
        # self.secondary_validation()

        
