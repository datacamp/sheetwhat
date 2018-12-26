

import pytest


from sheetwhat.Range import Range


@pytest.mark.parametrize("range_str", ["A1", "Z1", "A1:Z100", "AZFDDS124324"])
def test_constructor_str(range_str):
    Range(range_str)


@pytest.mark.parametrize(
    "range_dict",
    [
        {"startRowIndex": 0, "startColumnIndex": 0},
        {"startRowIndex": 21, "startColumnIndex": 0},
        {"startRowIndex": 21, "endRowIndex": 25, "startColumnIndex": 0},
        {"startRowIndex": 21, "startColumnIndex": 0, "endColumnIndex": 5},
        {
            "startRowIndex": 21,
            "endRowIndex": 25,
            "startColumnIndex": 0,
            "endColumnIndex": 5,
        },
    ],
)
def test_constructor_dict(range_dict):
    Range(range_dict)


@pytest.mark.parametrize(
    "range_dict",
    [
        {
            "startRowIndex": 21,
            "endRowIndex": 20,
            "startColumnIndex": 0,
            "endColumnIndex": 5,
        },
        {
            "startRowIndex": 21,
            "endRowIndex": 25,
            "startColumnIndex": 5,
            "endColumnIndex": 4,
        },
        {"startRowIndex": -21, "startColumnIndex": 0},
        {"startRowIndex": 21, "startColumnIndex": -5},
    ],
)
def test_constructor_dict_fail(range_dict):
    with pytest.raises(AssertionError):
        Range(range_dict)


@pytest.mark.parametrize("range_dict", [{}, [], lambda x: "bla"])
def test_constructor_dict_fail_key(range_dict):
    with pytest.raises(TypeError):
        Range(range_dict)


@pytest.mark.parametrize(
    "range_1_input, range_2_input, equals",
    [
        ("A1", "A1", True),
        ("A1", "B1", False),
        ("A1:B100", "A1:B100", True),
        ("A1:B100", "A1:B101", False),
        ("A1", {"startRowIndex": 0, "startColumnIndex": 0}, True),
        ({"startRowIndex": 0, "startColumnIndex": 0}, "A1", True),
        ({"startRowIndex": 1, "startColumnIndex": 0}, "A1", False),
        ({"startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0}, "A1", True),
        (
            {
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": 1,
            },
            "A1",
            True,
        ),
        (
            {
                "startRowIndex": 0,
                "endRowIndex": 4,
                "startColumnIndex": 0,
                "endColumnIndex": 3,
            },
            "A1:C4",
            True,
        ),
    ],
)
def test_equals(range_1_input, range_2_input, equals):
    assert (Range(range_1_input) == Range(range_2_input)) == equals


def test_equals_other_instance():
    assert Range("A1") != "other_type"


@pytest.mark.parametrize(
    "range_1_input, range_2_input, equals",
    [
        ("A1", "A1", True),
        ("A1", "B1", False),
        ("A1", "A1:A5", True),
        ("A1:A5", "A1:A4", False),
        ("A1:A5", "A1:B100", True),
        ("A1:A5", "B1:B5", False),
        ("A1:A5", "A1:A5", True),
    ],
)
def test_is_within(range_1_input, range_2_input, equals):
    assert (Range(range_1_input).is_within(Range(range_2_input))) == equals


def test_is_wihtin_other_instance():
    assert not (Range("B1").is_within("other_type"))
