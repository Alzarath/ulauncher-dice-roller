from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from collections.abc import Iterable

from lib.Segment import Segment, Operation
from lib.NumericValue import NumericValue
from lib.DiceRoller import DiceRoller, FudgeDiceRoller

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

def group_dice_content(values) -> None:
    group_operated_content(values, ["d"])
    group_appended_content(values, ["kh", "kl"])
    split_dice_content(values, ["kh", "kl"])

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

def split_dice_content(values, operators: Iterable, separators = "+-*/") -> None:
    should_process = False
    if len(values) == 1:
        inner_values = values[0]
    else:
        inner_values = values
    for value in inner_values:
        if value in operators:
            should_process = True
            break

    if should_process:
        i = 0
        new_values = []

        while i < len(inner_values):
            value = inner_values[i]
            if isinstance(value, list) and "d" in value:
                new_values = []
                for _ in range(int(value[0]) if len(value) > 2 else 1):
                    new_values.append([ "d", value[2] if len(value) > 2 else value[1]])
                inner_values.pop(i)
                for new_value in new_values:
                    inner_values.append(new_value)

            i += 1

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

def create_segments_from_content(values) -> NumericValue:
    if not isinstance(values, Iterable) or isinstance(values, str):
        return NumericValue(float(values))

    item: NumericValue | None = None

    # Determine item type
    if "d" in values:
        dice_values = []
        for item in values:
            try:
                dice_values.append(int(item))
            except:
                if item == "d":
                    pass
                else:
                    dice_values.append(item)

        dice_count: NumericValue = None
        dice_sides: NumericValue = None
        fudge_dice: bool = False
        if len(dice_values) == 2:
            dice_count = create_segments_from_content(dice_values[0])

            if dice_values[1] == "F":
                fudge_dice = True
            else:
                dice_sides = create_segments_from_content(dice_values[1])
        elif len(dice_values) == 1:
            dice_count = NumericValue(1)

            if dice_values[0] == "F":
                fudge_dice = True
            else:
                dice_sides = create_segments_from_content(dice_values[0])
        else:
            raise ValueError("Not enough arguments to form a dice.")

        if fudge_dice:
            item = FudgeDiceRoller(dice_count)
        else:
            item = DiceRoller(dice_count, dice_sides)
    else:
        item = Segment([])
        for value in values:
            match value:
                case "*":
                    item.operation = Operation.MULTIPLY
                case "/":
                    item.operation = Operation.DIVIDE
                case "-":
                    item.operation = Operation.SUBTRACT
                case "+":
                    item.operation = Operation.ADD
                case "kh":
                    item.operation = Operation.MAX
                case "kl":
                    item.operation = Operation.MIN
                case _:
                    item.append(create_segments_from_content(value))

    return item

def render_result(from_string):
    segments = create_segments_from_content(parse_string(from_string))
    result = float(str(segments.value))
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
