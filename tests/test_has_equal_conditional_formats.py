import pytest
from copy import deepcopy
from tests.helper import Identity, Mutation, setup_state, verify_success

from sheetwhat.checks import has_equal_conditional_formats

# Fixtures
@pytest.fixture()
def conditional_format():
    return [
        {
            "ranges": [
                {
                    "sheetId": "Sheet1",
                    "endRowIndex": 12,
                    "startRowIndex": 2,
                    "endColumnIndex": 8,
                    "startColumnIndex": 5,
                }
            ],
            "booleanRule": {
                "format": {
                    "backgroundColor": {
                        "red": 0.7176471,
                        "blue": 0.8039216,
                        "green": 0.88235295,
                    }
                },
                "condition": {
                    "type": "NUMBER_GREATER_THAN_EQ",
                    "values": [{"userEnteredValue": "25"}],
                },
            },
        }
    ]


@pytest.fixture()
def conditional_format_2(conditional_format):
    return [
        *conditional_format,
        {
            "ranges": [
                {
                    "sheetId": "Sheet1",
                    "endRowIndex": 12,
                    "startRowIndex": 2,
                    "endColumnIndex": 8,
                    "startColumnIndex": 5,
                }
            ],
            "gradientRule": {
                "minpoint": {
                    "color": {
                        "red": 0.34117648,
                        "green": 0.73333335,
                        "blue": 0.5411765,
                    },
                    "type": "MIN",
                },
                "maxpoint": {"color": {"red": 1, "green": 1, "blue": 1}, "type": "MAX"},
            },
        },
    ]


@pytest.fixture()
def solution_data(conditional_format):
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
        "conditionalFormats": conditional_format,
    }


@pytest.fixture()
def solution_data_2(conditional_format_2):
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
        "conditionalFormats": conditional_format_2,
    }


# Tests
@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (
            Mutation(
                ["conditionalFormats", 0, "booleanRule", "condition", "type"],
                "other condition",
            ),
            False,
            "condition of the first rule is incorrect",
        ),
        (
            Mutation(
                [
                    "conditionalFormats",
                    0,
                    "booleanRule",
                    "format",
                    "backgroundColor",
                    "red",
                ],
                0,
            ),
            False,
            "format of the first rule is incorrect",
        ),
        (
            Mutation(["conditionalFormats", 0], {"gradientRule": {}}),
            False,
            "single color",
        ),
    ],
)
def test_has_equal_conditional_formats(solution_data, trans, correct, match):
    user_data = trans(deepcopy(solution_data))
    # sct_range is irrelevant in conditional formats
    s = setup_state(user_data, solution_data, "A1")
    with verify_success(correct, match=match):
        has_equal_conditional_formats(s)


@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (
            Mutation(["conditionalFormats", 1], {"booleanRule": {}}),
            False,
            "second .* color scale",
        ),
        (
            Mutation(
                ["conditionalFormats", 1, "gradientRule", "minpoint", "type"], "NUMBER"
            ),
            False,
            "minpoint .* second",
        ),
    ],
)
def test_has_equal_conditional_formats_2(solution_data_2, trans, correct, match):
    user_data = trans(deepcopy(solution_data_2))
    # sct_range is irrelevant in conditional formats
    s = setup_state(user_data, solution_data_2, "A1")
    with verify_success(correct, match=match):
        has_equal_conditional_formats(s)
