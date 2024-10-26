from lib.NumericValueObject import NumericValueObject
from enum import Enum, auto
from functools import reduce
from typing import Self

class Operation(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MAX = auto()
    MIN = auto()

class Segment(NumericValueObject[float]):
    @property
    def value(self) -> NumericValueObject:
        return self.process()

    @property
    def operation(self) -> Operation:
        return self._operation
    @operation.setter
    def operation(self, value: Operation):
        self._operation = value

    def process(self) -> NumericValueObject | Self:
        return_value: NumericValueObject = 0.0
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

    def __init__(self, values: list[NumericValueObject | Self] = [], operation: Operation = Operation.ADD) -> None:
        self.values = values
        self.operation = operation
