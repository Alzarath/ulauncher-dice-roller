class NumericValue[T]:
    @property
    def value(self) -> T:
        """Value that the object represents and that operations are perform on. Can be replaced with more complex logic."""
        return self._value
    @value.setter
    def value(self, value: T):
        self._value = value

    def __init__(self, value: T):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return other - self.value

    def __mult__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __truediv__(self, other):
        return self.value / other

    def __rtruediv__(self, other):
        return other / self.value

    def __mod__(self, other):
        return self.value % other

    def __rmod__(self, other):
        return other % self.value

    def __lt__(self, other):
        if isinstance(other, NumericValue):
            other = other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, NumericValue):
            other = other.value
        return self.value <= other

    def __eq__(self, other):
        if isinstance(other, NumericValue):
            other = other.value
        return self.value == other

    def __ne__(self, other):
        if isinstance(other, NumericValue):
            other = other.value
        return self.value != other

    def __gt__(self, other):
        if isinstance(other, NumericValue):
            other = other.value
        return self.value > other

    def __ge__(self, other) -> bool:
        if isinstance(other, NumericValue):
            other = other.value
        return self.value >= other
