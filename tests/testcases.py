"""
@author: Nathanael Jöhrmann
"""
import pytest
from enum import Enum, auto


@pytest.mark.filterwarnings('ignore::PytestCollectionWarning')
class TestCase(Enum):
    """
    Enumeration for selection test cases.
    """
    __test__=False
    ZERO = auto()
    TOOLARGE = auto()
    UNSELECTED = auto()
    SELECTED = auto()
    MIN = auto()
    MAX = auto()


class Data(list):
    @property
    def selected(self):  # use this value to select one entity
        return min(self)

    @property
    def unselected(self):
        assert max(self) > self.selected
        return max(self)

    @property
    def too_large(self):
        return max(self)+1

    @property
    def min(self):
        return min(self)

    @property
    def max(self):
        return max(self)

    def get_case_data(self, case):
        if case == TestCase.ZERO:
            return 0
        elif case == TestCase.TOOLARGE:
            return self.too_large
        elif case == TestCase.UNSELECTED:
            return self.unselected
        elif case == TestCase.SELECTED:
            return self.selected
        elif case == TestCase.MIN:
            return self.min
        elif case == TestCase.MAX:
            return self.max
        raise  # todo: specific exception
