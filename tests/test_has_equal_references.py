import pytest
from copy import deepcopy
from helper import Identity, Mutation, setup_state, verify_success, compose
from sheetwhat.checks import has_equal_references

# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=B1", 1, 1], ["=$C$2", "=B2:C5", 8]],
    }


@pytest.fixture()
def solution_data_normalize():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=     B1", 1, 1], ["=$c$2", "=       B2:C5", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Mutation(["formulas", 0, 0], "=  C1"), "A1", False),
        (Mutation(["formulas", 0, 0], "=  C1"), "B1", True),
        (Mutation(["formulas", 0, 1], "=  C1"), "A1", True),
        (Mutation(["formulas", 1, 0], "=  C1"), "A2", True),
        (Mutation(["formulas", 0, 0], "=  C1"), "B2", True),
        (Mutation(["formulas", 0, 0], "=  b1"), "A1", True),
        (Identity(), "B2", True),
        (Mutation(["formulas", 1, 1], "=    A1:A2"), "B2", False),
    ],
)
def test_check_reference(solution_data, trans, sct_range, correct):
    user_data = trans(deepcopy(solution_data))
    s = setup_state(user_data, solution_data, sct_range)
    with verify_success(correct):
        has_equal_references(s)


@pytest.mark.parametrize(
    "trans, sct_range, correct",
    [
        (Identity(), "A1", True),
        (Mutation(["formulas", 0, 0], "=  C1"), "A1", False),
        (Mutation(["formulas", 0, 0], "=  C1"), "B1", True),
        (Mutation(["formulas", 0, 1], "=  C1"), "A1", True),
        (Mutation(["formulas", 1, 0], "=  C1"), "A2", True),
        (Mutation(["formulas", 0, 0], "=  C1"), "B2", True),
        (Identity(), "B2", True),
        (Mutation(["formulas", 1, 1], "=    A1:A2"), "B2", False),
    ],
)
def test_check_reference_normalize(solution_data_normalize, trans, sct_range, correct):
    user_data = trans(deepcopy(solution_data_normalize))
    s = setup_state(user_data, solution_data_normalize, sct_range)
    with verify_success(correct):
        has_equal_references(s)
