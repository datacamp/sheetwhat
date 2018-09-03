import pytest
from copy import deepcopy
from utils import Identity, Mutation, try_exercise, compose


# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=$B$1", 1, 1], ["=C2", "=$B$2:$C$5", 8]],
    }


@pytest.fixture()
def solution_data_normalize():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=     $B$1", 1, 1], ["=c2", "=       $B$2:$c$5", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, correct, message_contains",
    [
        (Identity(), "A1", True, None),
        (Mutation(["formulas", 0, 0], "=  C1"), "A1", False, "reference to `$B$1`"),
        (Mutation(["formulas", 0, 0], "=  C1"), "B1", True, None),
        (Mutation(["formulas", 0, 1], "=  C1"), "A1", True, None),
        (Mutation(["formulas", 1, 1], "=  C1"), "B2", False, None),
        (Mutation(["formulas", 0, 1], "=  C1"), "A2", True, None),
        (Identity(), "B2", True, None),
        (
            Mutation(["formulas", 1, 1], "=    A1:A2"),
            "B2",
            False,
            "reference to `$B$2:$C$5`",
        ),
    ],
)
def test_check_absolute_references(
    solution_data, trans, sct_range, correct, message_contains
):
    user_data = trans(deepcopy(solution_data))
    sct = [{"range": sct_range, "sct": ["check_absolute_references"]}]
    result = try_exercise(solution_data, user_data, sct)

    assert result.get("success") == correct
    if message_contains is not None:
        assert result.get("message") is not None
        message = result.get("message")
        if isinstance(message_contains, list):
            assert all([x in message for x in message_contains])
        else:
            assert message_contains in message


@pytest.mark.parametrize(
    "trans, sct_range, correct, message_contains",
    [
        (Identity(), "A1", True, None),
        (Mutation(["formulas", 0, 0], "=  C1"), "A1", False, "reference to `$B$1`"),
        (Mutation(["formulas", 0, 0], "=  C1"), "B1", True, None),
        (Mutation(["formulas", 0, 1], "=  C1"), "A1", True, None),
        (Mutation(["formulas", 1, 1], "=  C1"), "B2", False, None),
        (Mutation(["formulas", 0, 1], "=  C1"), "A2", True, None),
        (Identity(), "B2", True, None),
        (
            Mutation(["formulas", 1, 1], "=    A1:A2"),
            "B2",
            False,
            "reference to `$B$2`",
        ),
    ],
)
def test_check_absolute_references_normalize(
    solution_data_normalize, trans, sct_range, correct, message_contains
):
    user_data = trans(deepcopy(solution_data_normalize))
    sct = [{"range": sct_range, "sct": ["check_absolute_references"]}]
    result = try_exercise(solution_data_normalize, user_data, sct)

    assert result.get("success") == correct
    if message_contains is not None:
        assert result.get("message") is not None
        message = result.get("message")
        if isinstance(message_contains, list):
            assert all([x in message for x in message_contains])
        else:
            assert message_contains in message
