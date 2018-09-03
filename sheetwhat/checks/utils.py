import re
import copy

RANGE_REGEX = r"([a-zA-Z]+)(\d+)(?:\:([a-zA-Z]+)(\d+))?"


def range_to_row_columns(range_spec):
    groups = re.search(RANGE_REGEX, range_spec)

    row_columns = {
        "start_row": int(groups.group(2)) - 1,
        "start_column": letters_to_numbers(groups.group(1)),
    }

    if groups.group(3) is not None:
        row_columns["end_column"] = letters_to_numbers(groups.group(3)) + 1
    else:
        row_columns["end_column"] = row_columns["start_column"] + 1

    if groups.group(4) is not None:
        row_columns["end_row"] = int(groups.group(4))
    else:
        row_columns["end_row"] = row_columns["start_row"] + 1

    return row_columns


BASE = 26
NUMBER_OF_FIRST = ord("A")


def letters_to_numbers(letters):
    letters_normalized = letters.upper()
    letters_length = len(letters_normalized)
    return (
        sum(
            [
                (ord(letter) - NUMBER_OF_FIRST + 1)
                * BASE ** (letters_length - index - 1)
                for index, letter in enumerate(letters_normalized)
            ]
        )
        - 1
    )


def crop_by_range(array_2d, range_spec):
    row_columns = range_to_row_columns(range_spec)
    row_range = array_2d[row_columns["start_row"] : row_columns["end_row"]]

    if len(row_range) == 0:
        return [[]]

    return copy.deepcopy(
        [
            array[row_columns["start_column"] : row_columns["end_column"]]
            for array in row_range
        ]
    )


def is_empty(x):
    if isinstance(x, list):
        return all([is_empty(el) for el in x])
    elif isinstance(x, (str, dict)):
        return len(x) == 0
    else:
        return x is None


def round_array_2d(array_2d, ndigits):
    round_value = lambda x: round(x, ndigits) if isinstance(x, (int, float)) else x
    return map_2d(round_value, array_2d)


def normalize_formula(formula):
    return re.sub(r"\s+", "", formula.lower()) if isinstance(formula, str) else formula


def normalize_array_2d(array_2d):
    return map_2d(normalize_formula, array_2d)


def map_2d(func, array_2d):
    return [[func(cell) for cell in row] for row in array_2d]
