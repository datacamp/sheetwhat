import pytest
from copy import deepcopy
from utils import Identity, Mutation, Deletion, setup_state, verify_success
from sheetwhat.checks import check_range, has_equal_value

@pytest.fixture()
def user_data_seed():
    return {
        "values": [[1, 1, 1], [1, 52, "b"]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }


@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Identity(), "Z10", False),
        (Mutation(["values", 0, 0], ""), "A1", False),
        (Mutation(["values", 0, 0], None), "A1", False),
    ],
)
def test_check_range(user_data_seed, trans, sct_range, correct):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data_seed, sct_range)
    with verify_success(correct):
        check_range(s, field="values", field_msg="value")

@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Identity(), "A1:B2", True),
        (Identity(), "A1:C2", True),
        (Identity(), "C2", True),
        (Mutation(["values", 0, 0], 5), "B1", True),
        (Mutation(["values", 0, 0], 5), "A1", False),
        (Mutation(["values", 1, 2], "c"), "A1:C2", False),
        (Mutation(["formulas", 0, 0], "=1+0"), "A1", True),
        (Mutation(["formulas", 0, 0], "=1+0"), "B1", True),
        (Mutation(["values", 0, 1], 5), "B1", False),
        (Mutation(["values", 1, 0], "test"), "A1:B2", False),
    ],
)
def test_has_equal_value(user_data_seed, trans, sct_range, correct):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data_seed, sct_range)
    with verify_success(correct):
        has_equal_value(s)


@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Mutation(["values", 0, 0], 1.001), "A1", False),
        (Mutation(["values", 0, 0], 1.00001), "A1", True),
        (Mutation(["values", 0, 1], 1.00001), "A1:B2", True),
    ],
)
def test_has_equal_value_precision(user_data_seed, trans, sct_range, correct):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data_seed, sct_range)
    with verify_success(correct):
        has_equal_value(s)
