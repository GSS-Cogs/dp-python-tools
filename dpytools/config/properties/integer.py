from typing import Optional

from .base import BaseProperty


class IntegerProperty(BaseProperty):
    # TODO: Is there any scenario where IntegerProperty should have regex?
    regex: Optional[str]
    min_val: Optional[int]
    max_val: Optional[int]

    def type_is_valid(self):
        """
        Validate that the property looks like
        its of the correct type 
        """
        try:
            int(self.value)
        except Exception as err:
            raise Exception(f"Cannot cast {self.name} value {self.value} to integer.") from err

    def secondary_validation_passed(self):
        """
        Non type based validation you might want to
        run against a configuration value of this kind.
        """
        if not self.value:
            raise ValueError(f"Integer value for {self.name} does not exist")
        
        if self.regex:
            # TODO - confirm the value matches the regex
            ...

        if self.min_val:
            assert self.value >= self.min_val

        if self.max_val:
            assert self.value <= self.max_val