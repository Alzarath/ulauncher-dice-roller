from lib.NumericValue import NumericValue
from enum import Enum, auto
from functools import reduce

class Operation(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MAX = auto()
    MIN = auto()

class Segment(NumericValue[float]):
    @property
    def value(self) -> NumericValue:
        return self.process()

    @property
    def operation(self) -> Operation:
        return self._operation
    @operation.setter
    def operation(self, value: Operation):
        self._operation = value

    def process(self) -> NumericValue:
        return_value: NumericValue = 0.0
        match self.operation:
            case Operation.ADD:
                return_value = reduce(lambda x, y: x + y, self.values)
            case Operation.SUBTRACT:
                return_value = reduce(lambda x, y: x - y, self.values)
            case Operation.MULTIPLY:
                return_value = reduce(lambda x, y: x * y, self.values)
            case Operation.DIVIDE:
                return_value = reduce(lambda x, y: x / y, self.values)
            case Operation.MAX:
                return_value = reduce(lambda x, y: max(x, y), self.values)
            case Operation.MIN:
                return_value = reduce(lambda x, y: min(x, y), self.values)
        return return_value

    def append(self, other):
        self.values.append(other)

    def __init__(self, values: list[NumericValue] = [], operation: Operation = Operation.ADD) -> None:
        self.values = values
        self.operation = operation
