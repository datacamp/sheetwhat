import pytest
from copy import deepcopy
from utils import try_exercise, compose


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
        "formulas": [["=     B1", 1, 1], ["=$c$2", "=       B2:c5", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "sct_range, reference, correct",
    [
        ("A1", "B1", True),
        ("A1", "B3", False),
        ("B3", "B1", False),
        ("A2", "C2", False),
        ("A2", "$C$2", True),
        ("B2", "B2:C5", True),
        ("B2", "B2: C5", False),
        ("B2", "B2: C5", False),
    ],
)
def test_check_reference(solution_data, sct_range, reference, correct):
    user_data = deepcopy(solution_data)
    sct = [{"range": sct_range, "sct": [f'check_reference(reference = "{reference}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


@pytest.mark.parametrize(
    "sct_range, reference, correct",
    [
        ("A1", "B1", True),
        ("A1", "B3", False),
        ("B3", "B1", False),
        ("A2", "C2", False),
        ("A2", "$C$2", True),
        ("B2", "B2:C5", True),
        ("B2", "B2: C5", False),
        ("B2", "B2: C5", False),
    ],
)
def test_check_reference_normalize(solution_data, sct_range, reference, correct):
    user_data = deepcopy(solution_data)
    sct = [{"range": sct_range, "sct": [f'check_reference(reference = "{reference}")']}]

    assert try_exercise(solution_data, user_data, sct)["success"] == correct


def test_check_reference_suggestion(solution_data):
    user_data = deepcopy(solution_data)
    sct = [{"range": "A1", "sct": ['check_reference(reference = "C1")']}]

    assert try_exercise(solution_data, user_data, sct)["message"].endswith(
        "Did you use a reference to `C1`?"
    )
