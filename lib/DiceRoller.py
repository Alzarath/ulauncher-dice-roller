from lib.NumericValue import NumericValue
import random

class DiceRoller(NumericValue[int]):
    @property
    def values(self) -> list[NumericValue]:
        """The results of each individual dice roll."""
        return self._values

    @property
    def min(self) -> NumericValue:
        """The minimum value that each dice can roll."""
        return NumericValue(1)

    @property
    def max(self) -> NumericValue:
        """The maximum value that each dice can roll."""
        return self._dice_sides

    def roll(self):
        """Generates a list of random integers and sets the overall value to the sum of them."""
        lower_range = self.min.value
        upper_range = self.max.value
        self._values = []

        for i in range(int(self._dice_count.value)):
            self._values.append(NumericValue(random.randrange(int(lower_range), int(upper_range)+1)))

        self.value = sum(self.values)

    def __init__(self, dice_count: NumericValue, dice_sides: NumericValue):
        self._dice_count = dice_count
        self._dice_sides = dice_sides
        self.roll()

class FudgeResult(NumericValue[int]):
    def __repr__(self):
        if self.value < 0:
            return abs(self.value) * "[-]"
        elif self.value > 0:
            return self.value * "[+]"

        return "[ ]"

class FudgeDiceRoller(DiceRoller):
    @property
    def min(self) -> NumericValue:
        """The minimum value that each dice can roll."""
        return NumericValue(-1)

    @property
    def max(self) -> NumericValue:
        """The maximum value that each dice can roll."""
        return NumericValue(1)

    @property
    def values(self) -> list[FudgeResult]:
        """The results of each individual dice roll."""
        return list(map(lambda x: FudgeResult(x), self._values))

    def __init__(self, dice_count: NumericValue = NumericValue(1)):
        super().__init__(dice_count, NumericValue(6))
