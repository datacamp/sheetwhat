import importlib
import pytest

from copy import deepcopy
from utils import Identity, Mutation, try_exercise

@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }

@pytest.mark.parametrize(
    "trans, sct_range, target",
    [
        (Mutation(["values", 0, 0], 5), "A1", "The value at <code>A1</code> is not correct."),
        (Mutation(["values", 0, 0], 5), "A1:B2", "The value at <code>A1:B2</code> is not correct."),
    ],
)
def test_check_value(solution_data, trans, sct_range, target):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": ["Ex().has_equal_value()"]}]
    assert try_exercise(solution_data, user_data, sct)["message"] == target

