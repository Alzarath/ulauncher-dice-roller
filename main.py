from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from enum import Enum, auto
from typing import Self
from collections.abc import Iterable

import random

class Operation(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MAX = auto()
    MIN = auto()
    ROLL = auto()

class Segment:
    @property
    def value(self) -> float:
        return_value = self
        while hasattr(return_value, 'process'):
            return_value = return_value.process()
        return return_value

    def process(self) -> float | Self:
        return_value: float = 0.0
        match self.operation:
            case Operation.ADD:
                for value in self.values:
                    return_value += value
            case Operation.SUBTRACT:
                if len(self.values) > 0:
                    return_value += self.values[0]
                for value in self.values[1:]:
                    return_value -= value
            case Operation.MULTIPLY:
                if len(self.values) > 0:
                    return_value += self.values[0]
                for value in self.values[1:]:
                    return_value *= value
            case Operation.DIVIDE:
                if len(self.values) > 0:
                    return_value += self.values[0]
                for value in self.values[1:]:
                    return_value /= value
            case Operation.MAX:
                if len(self.values) > 0:
                    return_value += self.values[0]
                for value in self.values[1:]:
                    return_value = max(value, return_value)
            case Operation.MIN:
                if len(self.values) > 0:
                    return_value += self.values[0]
                for value in self.values[1:]:
                    return_value = min(value, return_value)
            case Operation.ROLL:
                return_value = Segment()
                if len(self.values) == 1:
                    upper = int(self.values[0].value if hasattr(self.values[0], 'value') else self.values[0])+1
                    return_value.values.append(random.randrange(1, upper))
                elif len(self.values) == 2:
                    count = int(self.values[0].value if hasattr(self.values[0], 'value') else self.values[0])
                    upper = int(self.values[1].value if hasattr(self.values[1], 'value') else self.values[1])+1
                    for i in range(count):
                        return_value.values.append(random.randrange(1, upper))
                elif len(self.values) <= 0:
                    raise ValueError(f"Dice roll expected at least 1 argument, got {len(self.values)}")
                else:
                    raise ValueError(f"Dice roll expected at most 2 arguments, got {len(self.values)}")
        return return_value

    def append(self, other):
        self.values.append(other)
    
    def __init__(self, _values: list[float | Self] = [], _operation: Operation = Operation.ADD) -> None:
        self.values = _values.copy()
        self.operation = _operation

    def __repr__(self):
        return f"Segment({self.values}, {self.operation})"

    def __add__(self, other) -> float:
        return self.value + other

    def __radd__(self, other) -> float:
        return other + self.value

    def __sub__(self, other) -> float:
        return self.value - other
    
    def __rsub__(self, other) -> float:
        return other - self.value

    def __mult__(self, other) -> float:
        return self.value * other
    
    def __rmul__(self, other) -> float:
        return other * self.value

    def __truediv__(self, other) -> float:
        return self.value / other
    
    def __rtruediv__(self, other) -> float:
        return other / self.value
    
    def __mod__(self, other) -> float:
        return self.value % other
    
    def __rmod__(self, other) -> float:
        return other % self.value

    def __eq__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value == other

    def __lt__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value < other

    def __le__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value <= other

    def __eq__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value == other

    def __ne__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value != other

    def __gt__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value > other

    def __ge__(self, other) -> bool:
        if hasattr(other, 'value'):
            other = other.value
        return self.value >= other

def parse_string(argument):
    values = []
    current_value = ""
    bracket_depth = 0
    i = 0
    while i < len(argument):
        char = argument[i]
        if char == "(":
            bracket_depth += 1
        elif bracket_depth > 0:
            if char == "(":
                bracket_depth += 1
                current_value += char
            if char == ")":
                bracket_depth -= 1
                if bracket_depth > 0:
                    current_value += char
                else:
                    values.append(parse_string(current_value)[0])
                    current_value = ""
            else:
                current_value += char
        elif char in "d+-*/":
            if current_value != "":
                values.append(current_value)
            values.append(char)
            current_value = ""
        elif i < len(argument)-1 and (char+argument[i+1] == "kh" or char+argument[i+1] == "kl"):
            if current_value != "":
                values.append(current_value)
                current_value = ""
            values.append(char+argument[i+1])
            i += 1
        else:
            current_value += char
        i += 1
    
    if current_value != "":
        values.append(current_value)
    
    group_dice_content(values)
    group_arithmetic_content(values)

    return values

def string_to_num(string):
    string = string.replace(',', '.')
    
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            raise ValueError

def render_result(from_string):
    result = create_segments_from_content(parse_string(from_string)).value
    if result % 1 == 0:
        result = int(result)
    data = {'roll_string': from_string}        

    return RenderResultListAction([
        ExtensionResultItem(icon='images/icon.png',
                            name=f'{result}',
                            description=f'Number rolled from {from_string} resulted in {result}',
                            on_enter=CopyToClipboardAction(str(result))),
        ExtensionResultItem(icon='images/icon.png',
                            name='Reroll',
                            description='Reroll using the same values',
                            on_enter=ExtensionCustomAction(data, keep_app_open=True))
        ])

def group_dice_content(values) -> None:
    group_operated_content(values, ["d"])
    group_appended_content(values, ["kh", "kl"])

def group_arithmetic_content(values) -> None:
    group_operated_content(values, ["*", "/"])
    group_operated_content(values, ["+", "-"])

def group_operated_content(values, operators: Iterable, separators = "+-*/") -> None:
    i = 0
    while i < len(values):
        value = values[i]
        offset = 0
        if value in operators:
            new_value = []

            if i < len(values)-1:
                new_value.append(values.pop(i+1))

            new_value.append(values.pop(i))

            if i > 0 and (isinstance(values[i-1], list) or values[i-1] not in separators):
                new_value.append(values.pop(i-1))
                offset -= 1
            
            # Values are acquired front to back so we don't have to continuously offset.
            # As a result, we need to reverse the list.
            new_value.reverse()
            values.insert(i+offset, new_value)
        
        i += 1 + offset

def group_appended_content(values, operators: Iterable, separators = "+-*/") -> None:
    i = 0
    while i < len(values):
        value = values[i]
        offset = 0
        if value in operators:
            new_value = []

            new_value.append(values.pop(i))

            if i > 0 and (isinstance(values[i-1], list) or values[i-1] not in separators):
                new_value.append(values.pop(i-1))
                offset -= 1
            
            # Values are acquired front to back so we don't have to continuously offset.
            # As a result, we need to reverse the list.
            new_value.reverse()
            values.insert(i+offset, new_value)

        i += 1 + offset

def create_segments_from_content(values) -> Segment:
    segments = Segment()
    for item in values:
        match item:
            case "*":
                segments.operation = Operation.MULTIPLY
            case "/":
                segments.operation = Operation.DIVIDE
            case "-":
                segments.operation = Operation.SUBTRACT
            case "+":
                segments.operation = Operation.ADD
            case "d":
                segments.operation = Operation.ROLL
            case "kh":
                segments.operation = Operation.MAX
            case "kl":
                segments.operation = Operation.MIN
            case _:
                if isinstance(item, list):
                    segments.append(create_segments_from_content(item))
                else:
                    segments.append(float(item))
    
    return segments

class DiceRollerExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        roll_string = event.get_argument() or extension.preferences.get('default_roll')

        return render_result(roll_string)

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        return render_result(data['roll_string'])


if __name__ == '__main__':
    DiceRollerExtension().run()
    