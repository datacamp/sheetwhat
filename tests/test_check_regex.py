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
    "trans, sct_range, pattern, correct",
    [
        (Identity(), "A1", "=0", True),
        (Identity(), "A1:A2", "=", True),
        (Mutation(["formulas", 0, 0], "= 1 + 0"), "A1", "=1+0", False),
        (Mutation(["values", 1, 1], "test"), "B2", "test", False),
        (Mutation(["formulas", 1, 1], "test"), "B2", "test", True),
        (Mutation(["formulas", 0, 1], "testtesttest"), "B1", "^(?:test)+$", True),
        (Mutation(["formulas", 0, 1], ""), "B1", "^(?:test)+$", False),
        (
            compose(
                Mutation(["formulas", 0, 0], "=0+0"),
                Mutation(["formulas", 0, 1], "=1+0"),
                Mutation(["formulas", 1, 0], "=0+1"),
                Mutation(["formulas", 1, 1], "=1-1"),
                Mutation(["values", 0, 0], 0),
                Mutation(["values", 0, 1], 1),
                Mutation(["values", 1, 0], 1),
                Mutation(["values", 1, 1], 2),
            ),
            "A1:B2",
            "1|0 +|- 1|0",
            True,
        ),
    ],
)
def test_check_regex(solution_data, trans, sct_range, pattern, correct):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": [f'check_regex(pattern = "{pattern}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct
