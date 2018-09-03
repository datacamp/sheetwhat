import pytest

from sheetwhat.checks.utils import (
    letters_to_numbers,
    range_to_row_columns,
    crop_by_range,
)


@pytest.mark.parametrize(
    "letters, number",
    [
        ("A", 0),
        ("B", 1),
        ("Z", 25),
        ("a", 0),
        ("b", 1),
        ("z", 25),
        ("AA", 26),
        ("AZ", 51),
        ("BA", 52),
        ("AUY", 1246),
        ("AUZ", 1247),
        ("auz", 1247),
    ],
)
def test_letters_to_numbers(letters, number):
    assert letters_to_numbers(letters) == number


@pytest.mark.parametrize(
    "range_spec, start_row, start_column, end_row, end_column",
    [
        ("A1", 0, 0, 1, 1),
        ("B1", 0, 1, 1, 2),
        ("A1:A2", 0, 0, 2, 1),
        ("A1:B1", 0, 0, 1, 2),
        ("A1:B2", 0, 0, 2, 2),
    ],
)
def test_range_to_row_columns(range_spec, start_row, start_column, end_row, end_column):
    assert range_to_row_columns(range_spec) == {
        "start_row": start_row,
        "start_column": start_column,
        "end_row": end_row,
        "end_column": end_column,
    }


@pytest.mark.parametrize(
    "array_2d, range_spec, target",
    [
        ([[0, 1, 2], [3, 4, 5]], "A1", [[0]]),
        ([[0, 1, 2], [3, 4, 5]], "A1:A2", [[0], [3]]),
        ([[0, 1, 2], [3, 4, 5]], "A1:B1", [[0, 1]]),
        ([[0, 1, 2], [3, 4, 5]], "A1:B2", [[0, 1], [3, 4]]),
        ([[0, 1, 2], [3, 4, 5]], "Z1", [[]]),
    ],
)
def test_crop_by_range(array_2d, range_spec, target):
    assert crop_by_range(array_2d, range_spec) == target


def test_crop_by_range_deepcopy():
    obj = {"test": "what"}
    b = crop_by_range([[obj]], "A1")
    b[0][0]["test"] = "that"
    assert obj["test"] == "what"
