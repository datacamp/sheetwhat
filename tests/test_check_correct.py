import pytest
from copy import deepcopy
from utils import Identity, Mutation, try_exercise, compose


# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, check, diagnose, correct, message_contains",
    [
        (Identity(), "A1", "check_value", "check_formula", True, None),
        (Identity(), "A2", "check_formula", "check_value", True, None),
        (
            Mutation(["formulas", 0, 0], "=1"),
            "A1",
            "check_value",
            "check_formula",
            True,
            None,
        ),
        (
            Mutation(["formulas", 0, 0], "=1"),
            "A1",
            "check_formula",
            "check_value",
            False,
            "The formula at `A1` is not correct",
        ),
        (
            compose(Mutation(["formulas", 0, 0], "=2"), Mutation(["values", 0, 0], 2)),
            "A1",
            "check_value",
            "check_formula",
            False,
            "The formula at `A1` is not correct",
        ),
    ],
)
def test_check_correct(
    solution_data, trans, sct_range, check, diagnose, correct, message_contains
):
    user_data = trans(deepcopy(solution_data))
    sct = [
        {
            "range": sct_range,
            "sct": [f"check_correct(check={check}, diagnose={diagnose})"],
        }
    ]

    result = try_exercise(solution_data, user_data, sct)

    assert result.get("success") == correct
    if message_contains is not None:
        assert result.get("message") is not None and message_contains in result.get(
            "message"
        )
