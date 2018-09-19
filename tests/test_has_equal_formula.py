import pytest
from copy import deepcopy
from tests.helper import Identity, Mutation, setup_state, verify_success
from sheetwhat.checks import has_equal_formula

# Fixtures
@pytest.fixture()
def user_data_seed():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }


@pytest.fixture()
def user_data_norm_seed():
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
def test_has_equal_formula(user_data_seed, trans, sct_range, correct):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data_seed, sct_range)
    with verify_success(correct):
        has_equal_formula(s)


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
    user_data_norm_seed, trans, sct_range, correct
):
    user_data = trans(deepcopy(user_data_norm_seed))
    s = setup_state(user_data, user_data_norm_seed, sct_range)
    with verify_success(correct):
        has_equal_formula(s)
