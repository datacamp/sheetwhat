import pytest
from copy import deepcopy
from utils import Identity, Mutation, try_exercise, compose


# Fixtures
@pytest.fixture()
def solution_data():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=SUM(B2:B5)", 1, 1], ["=1+0", "=52", 8]],
    }


problem_message = ["problem", "correctness test", "support"]

# Tests
@pytest.mark.parametrize(
    "sct, correct, message_contains",
    [
        ("chek_formula", False, problem_message),
        ("check_function(function = 'SUM'", False, problem_message),
        ("check_function('SUM')", False, problem_message),
        ("check_function(function = 'SUM')", True, None),
        ('check_function(function = "SUM")', True, None),
        ("check_function(function = \"SUM')", False, problem_message),
        ('check_function(func = "SUM")', True, None),
        ('check_function(function = "SUM", ,)', False, problem_message),
        ('check_function(function = "SUM" ,)', True, None),
        ('{ check_function(function = "SUM" ,) }', True, None),
        ('{ check_function(function = "SUM" ,); check_value }', True, None),
        ('{ check_function(function = "SUM" ,), check_value }', False, problem_message),
        ("check_correct(check = check_value, diagnose = check_formula)", True, None),
        (
            """
            check_correct(
                check = {
                    check_value
                },
                diagnose = {
                    check_formula;
                    check_function(function = 'SUM')
                }
            )
            """,
            True,
            None,
        ),
        (["check_value", "check_formula"], True, None),
        ("check_value check_formula", False, problem_message),
        ("check_function(function = 'SUM'')", False, problem_message),
        ("check_function(function = 'SUM\\'')", False, ["formula at `A1`", "SUM'()"]),
    ],
)
def test_check_absolute_references(solution_data, sct, correct, message_contains):
    user_data = deepcopy(solution_data)
    if isinstance(sct, list):
        sct = [{"range": "A1", "sct": sct}]
    else:
        sct = [{"range": "A1", "sct": [sct]}]
    result = try_exercise(solution_data, user_data, sct)

    assert result.get("success") == correct
    if message_contains is not None:
        assert result.get("message") is not None
        message = result.get("message")
        if isinstance(message_contains, list):
            assert all([x in message for x in message_contains])
        else:
            assert message_contains in message
