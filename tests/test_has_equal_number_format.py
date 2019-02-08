import pytest
from copy import deepcopy
from tests.helper import Identity, Mutation, setup_state, verify_success
from sheetwhat.checks import has_equal_number_format

# Fixtures
@pytest.fixture()
def user_data_seed():
    return {
        "numberFormats": [
            [
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ],
            [
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ],
            [
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ],
            [
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ],
            [
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ],
            [
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ],
        ]
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, correct, match",
    [
        (Identity(), "A1", True, None),
        (Identity(), "A1:B2", True, None),
        (
            Mutation(
                ["numberFormats", 0, 0],
                {"numberFormat": {"type": "NUMBER", "pattern": "0.00"}},
            ),
            "A1",
            True,
            None,
        ),
        (
            Mutation(["numberFormats", 1, 0, "numberFormat", "type"], "TEXT"),
            "A2",
            False,
            "Expected a number, but got text",
        ),
        (
            Mutation(["numberFormats", 0, 1, "numberFormat", "type"], "UNKONWN"),
            "B1",
            False,
            "In cell `B1`, did you use the correct number format?",
        ),
        (
            Mutation(["numberFormats", 1, 1, "numberFormat", "patter"], "0.0"),
            "B2",
            False,
            "In cell `B2`, did you use the correct number format?",
        ),

    ],
)
def test_has_equal_number_format(user_data_seed, trans, sct_range, correct, match):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data_seed, sct_range)
    with verify_success(correct, match=match):
        has_equal_number_format(s)
