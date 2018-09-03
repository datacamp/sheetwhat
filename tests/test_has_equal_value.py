import pytest
from copy import deepcopy
from utils import Identity, Mutation, Deletion, try_exercise

@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 'b']],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }

@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Identity(), "Z10", True),
        (Mutation(["values", 0, 0], ""), "A1", False),
        (Mutation(["values", 0, 0], None), "A1", False)
    ]
)
def test_check_range(solution_data, trans, sct_range, correct):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": ["Ex().check_range()"]}]
    assert try_exercise(solution_data, user_data, sct)["success"] == correct

@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Identity(), "A1:B2", True),
        (Identity(), "A1:C2", True),
        (Identity(), "C2", True),
        (Mutation(["values", 0, 0], 5), "B1", True),
        (Mutation(["values", 0, 0], 5), "A1", False),
        (Mutation(["values", 1, 2], 'c'), "A1:C2", False),
        (Mutation(["formulas", 0, 0], "=1+0"), "A1", True),
        (Mutation(["formulas", 0, 0], "=1+0"), "B1", True),
        (Mutation(["values", 0, 1], 5), "B1", False),
        (Mutation(["values", 1, 0], "test"), "A1:B2", False),
    ],
)
def test_has_equal_value(solution_data, trans, sct_range, correct):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": ["Ex().has_equal_value()"]}]
    assert try_exercise(solution_data, user_data, sct)["success"] == correct

@pytest.mark.parametrize(
   "trans, sct_range, correct",
   [
       (Mutation(["values", 0, 0], 1.001), "A1", False),
       (Mutation(["values", 0, 0], 1.00001), "A1", True),
       (Mutation(["values", 0, 1], 1.00001), "A1:B2", True),
   ],
)
def test_has_equal_value_precision(solution_data, trans, sct_range, correct):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": ["Ex().has_equal_value()"]}]
    assert try_exercise(solution_data, user_data, sct)["success"] == correct
