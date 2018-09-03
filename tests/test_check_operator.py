import pytest
from copy import deepcopy
from utils import try_exercise, compose


# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=1+1", 1, 1], ["=3*5", "=B2/B5", 8]],
    }


@pytest.fixture()
def solution_data_normalize():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=     1 + 1", 1, 1], ["=3*5", "=       b2/B5", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "sct_range, operator, correct",
    [
        ("A1", "+", True),
        ("A1", "-", False),
        ("B3", "*", False),
        ("A2", "/", False),
        ("A2", "*", True),
        ("B2", "/", True),
        ("B2", "  / ", False),
        ("B2", " /", False),
    ],
)
def test_check_operator(solution_data, sct_range, operator, correct):
    user_data = deepcopy(solution_data)
    sct = [{"range": sct_range, "sct": [f'check_operator(operator = "{operator}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


@pytest.mark.parametrize(
    "sct_range, operator, correct",
    [
        ("A1", "+", True),
        ("A1", "-", False),
        ("B3", "*", False),
        ("A2", "/", False),
        ("A2", "*", True),
        ("B2", "/", True),
        ("B2", "  / ", False),
        ("B2", " /", False),
    ],
)
def test_check_operator_normalize(solution_data, sct_range, operator, correct):
    user_data = deepcopy(solution_data)
    sct = [{"range": sct_range, "sct": [f'check_operator(operator = "{operator}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


def test_check_operator_suggestion(solution_data):
    user_data = deepcopy(solution_data)
    sct = [{"range": "A1", "sct": ['check_operator(operator = "/")']}]

    assert try_exercise(solution_data, user_data, sct)["message"].endswith(
        "Did you use the `/` operator?"
    )
