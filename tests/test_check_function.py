import pytest
from copy import deepcopy
from tests.helper import verify_success, setup_state
from sheetwhat.checks import check_function

# Fixtures
@pytest.fixture()
def user_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=SUM(A1)", 1, 1], ["=AVERAGE($C$2)", "=MEDIAN(B2:C5)", 8]],
    }


@pytest.fixture()
def user_data_normalize():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [
            ["=     SUM(B1)", 1, 1],
            ["=average($c$2)", "=       mEdIaN(B2:c5)", 8],
        ],
    }


@pytest.fixture()
def user_data_index():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [
            ["=SUM(A1) + SUM(A1)", 1, 1],
            ["=    aVeRaGe($C$2) + average($C$2)", "=MEDIAN(B2:C5) + MEDIAN(B2:C5)"]
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
def test_check_function(user_data, sct_range, function, correct):
    s = setup_state(user_data, user_data, sct_range)
    with verify_success(correct):
        check_function(s, name=function)


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
def test_check_function_normalize(user_data_normalize, sct_range, function, correct):
    s = setup_state(user_data_normalize, user_data_normalize, sct_range)
    with verify_success(correct):
        check_function(s, name=function)


@pytest.mark.parametrize(
    "sct_range, function, index, correct",
    [
        ("A1", "SUM", 0, True),       # 1
        ("A1", "TEST", 0, False),     # 0
        ("A1", "SUM", 1, True),       # 1
        ("A1", "SUM", 2, False),      # 0
        ("A1", "TEST", 1, False),     # 0
        ("A2", "AVERAGE", 0, True),   # 1
        ("A2", "AVERAGE", 1, True),   # 1
        ("A2", "AVERAGE", 2, False),  # 0
        ("B2", "MEDIAN", 0, True),    # 1
        ("B2", "MEDIAN", 1, True),    # 1
        ("B2", "MEDIAN", 2, False),   # 0
        ("B2", "TEST", 0, False),     # 0
        ("B2", "TEST", 1, False),     # 0
        ("B2", "TEST", 2, False),     # 0
        ("B2", "SUM", 0, False),      # 0
    ]
)
def test_check_function_index(user_data_index, sct_range, function, index, correct):
    s = setup_state(user_data_index, user_data_index, sct_range)
    with verify_success(correct):
        check_function(s, name=function, index=index)
