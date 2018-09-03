import pytest
from copy import deepcopy
from utils import try_exercise, compose


# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=SUM(A1)", 1, 1], ["=AVERAGE($C$2)", "=MEDIAN(B2:C5)", 8]],
    }


@pytest.fixture()
def solution_data_normalize():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [
            ["=     SUM(B1)", 1, 1],
            ["=average($c$2)", "=       mEdIaN(B2:c5)", 8],
        ],
    }


# Tests
@pytest.mark.parametrize(
    "sct_range, function, correct",
    [
        ("A1", "SUM", True),
        ("A1", "TEST", False),
        ("C2", "VAR", False),
        ("B3", "VAR", False),
        ("A2", "EXP", False),
        ("A2", "AVERAGE", True),
        ("B2", "MEDIAN", True),
        ("B2", "median", True),
        ("B2", " M eDIAn", True),
    ],
)
def test_check_function(solution_data, sct_range, function, correct):
    user_data = deepcopy(solution_data)
    sct = [{"range": sct_range, "sct": [f'Ex().check_function(name = "{function}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


@pytest.mark.parametrize(
    "sct_range, function, correct",
    [
        ("A1", "SUM", True),
        ("A1", "TEST", False),
        ("B3", "VAR", False),
        ("A2", "EXP", False),
        ("A2", "AVERAGE", True),
        ("B2", "MEDIAN", True),
        ("B2", "median", True),
        ("B2", " M eDIAn", True),
    ],
)
def test_check_function_normalize(solution_data, sct_range, function, correct):
    user_data = deepcopy(solution_data)
    sct = [{"range": sct_range, "sct": [f'Ex().check_function(name = "{function}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


# TODO: part of messaging
# def test_check_function_suggestion(solution_data):
#    user_data = deepcopy(solution_data)
#    sct = [{"range": "A1", "sct": ['Ex().check_function(name = "AVERAGE")']}]
#
#    assert try_exercise(solution_data, user_data, sct)["message"].endswith(
#        "Did you use the `AVERAGE()` function?"
#    )
