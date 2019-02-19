import pytest
from copy import deepcopy
from tests.helper import Identity, Mutation, setup_state, verify_success
from sheetwhat.checks import has_equal_data_validation

# Fixtures
@pytest.fixture()
def user_data_seed():
    return {
        "dataValidations": [
            [
                {
                    "condition": {
                        "type": "NUMBER_BETWEEN",
                        "values": [
                            {"userEnteredValue": "1"},
                            {"userEnteredValue": "10"},
                        ],
                    }
                }
            ]
        ]
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, correct, match",
    [
        (Identity(), "A1", True, None),
        (
            Mutation(
                ["dataValidations", 0, 0, "condition", "type"], "NUMBER_NOT_BETWEEN"
            ),
            "A1",
            False,
            "In cell `A1`, did you use the correct data validation?",
        ),
        (Mutation(["dataValidations", 0, 0, "strict"], True), "A1", True, None),
        (
            Mutation(
                ["dataValidations", 0, 0, "condition", "values", 0, "userEnteredValue"],
                "1",
            ),
            "A1",
            True,
            None,
        ),
        (
            Mutation(
                ["dataValidations", 0, 0, "condition", "values", 0, "userEnteredValue"],
                5,
            ),
            "A1",
            False,
            "In cell `A1`, did you use the correct data validation?",
        ),
    ],
)
def test_has_equal_data_validation(user_data_seed, trans, sct_range, correct, match):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data_seed, sct_range)
    with verify_success(correct, match=match):
        has_equal_data_validation(s)
