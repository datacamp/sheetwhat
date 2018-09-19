import pytest
from copy import deepcopy
from tests.helper import setup_state, verify_success
from sheetwhat.checks import check_operator

# Fixtures
@pytest.fixture()
def user_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=1+1", 1, 1], ["=3*5", "=B2/B5", 8]],
    }


@pytest.fixture()
def user_data_normalize():
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
        ("B2", "  / ", True),
        ("B2", " /", True),
    ],
)
def test_check_operator(user_data, sct_range, operator, correct):
    s = setup_state(user_data, user_data, sct_range)
    with verify_success(correct):
        check_operator(s, operator=operator)


@pytest.mark.parametrize(
    "sct_range, operator, correct",
    [
        ("A1", "+", True),
        ("A1", "-", False),
        ("B3", "*", False),
        ("A2", "/", False),
        ("A2", "*", True),
        ("B2", "/", True),
        ("B2", "  / ", True),
        ("B2", " /", True),
    ],
)
def test_check_operator_normalize(user_data_normalize, sct_range, operator, correct):
    s = setup_state(user_data_normalize, user_data_normalize, sct_range)
    with verify_success(correct):
        check_operator(s, operator=operator)
