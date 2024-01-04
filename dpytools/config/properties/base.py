from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Union, Tuple, Optional

@dataclass
class BaseProperty(metaclass=ABCMeta):
    name: str
    value: Any

    # TODO: getter
    # allow someone to get the property

    # TODO: setter
    # categorically disallow anyone from
    # changing a property after the class
    # has been instantiated.
    # Refuse to do it, and log an error.

    @abstractmethod
    def type_is_valid(self):
        """
        Validate that the property looks like
        its of the correct type 
        """
        ...

    # Note: Won't apply to all types so its not
    # an abstract method, its just a normal method
    # we can overwrite where relevant.
    def secondary_validation(self):
        """
        Non type based validation you might want to
        run against a configuration value.
        """
        ...