from typing import Optional

from base import BaseProperty


class StringProperty(BaseProperty):
    regex: Optional[str]
    min_len: Optional[int]
    max_len: Optional[int]

    def type_is_valid(self):
        """
        Validate that the property looks like
        its of the correct type 
        """
        try:
            str(self.value)
        except Exception as err:
            raise Exception(f"Cannot cast {self.name} value {self.value} to string.") from err

    def secondary_validation_passed(self):
        """
        Non type based validation you might want to
        run against a configuration value of this kind.
        """
        if len(self.value) == 0:
            raise ValueError(f"Str value for {self.name} is an empty string")
        
        if self.regex:
            # TODO - confirm the value matches the regex
            ...

        if self.min_len:
            # TODO - confirm the string matches of exceeds the minimum length
            ...

        if self.max_len:
            # TODO - confirm the value matches or is less than the max length
            ...