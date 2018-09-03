import pytest
from copy import deepcopy
from utils import Identity, Mutation, try_exercise


# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }


@pytest.fixture()
def solution_data_normalize():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=SUM(A1:C1)", 1, 1], ["=   AVaragE(A1)", "=52", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Identity(), "A1:B2", True),
        (Mutation(["values", 0, 0], 5), "B1", True),
        (Mutation(["values", 0, 0], 5), "A1", True),
        (Mutation(["formulas", 0, 0], "=1+0"), "A1", False),
        (Mutation(["formulas", 0, 0], "=1+0"), "B1", True),
        (Mutation(["values", 0, 1], 5), "B1", True),
        (Mutation(["values", 1, 0], "test"), "A1:B2", True),
    ],
)
def test_has_equal_formula(solution_data, trans, sct_range, correct):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": ["Ex().has_equal_formula()"]}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Mutation(["formulas", 0, 0], "=     SUM(A1:C1)"), "A1", True),
        (Mutation(["formulas", 0, 0], "=sum(A1:C1)"), "A1", True),
        (Mutation(["formulas", 0, 0], "=  sUm(A1:C1)"), "A1", True),
        (Mutation(["formulas", 0, 0], "=   Sunn(A1:C1)"), "A1", False),
        (Mutation(["formulas", 0, 1], "=aVaRaGe(A1)"), "A2", True),
    ],
)
def test_has_equal_formula_normalization(
    solution_data_normalize, trans, sct_range, correct
):
    user_data = trans(deepcopy(solution_data_normalize))
    sct = [{"range": sct_range, "sct": ["Ex().has_equal_formula()"]}]

    assert try_exercise(solution_data_normalize, user_data, sct)["success"] == correct
