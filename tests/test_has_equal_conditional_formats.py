import pytest
from copy import deepcopy
from tests.helper import (
    compose,
    Addition,
    Deletion,
    Identity,
    Mutation,
    setup_state,
    setup_ex_state,
    verify_success,
)

from sheetwhat.checks import has_equal_conditional_formats

# Fixtures
@pytest.fixture()
def conditional_format():
    return [
        {
            "ranges": [
                {
                    "sheetId": "Sheet1",
                    # A1:C4
                    "endRowIndex": 4,
                    "startRowIndex": 0,
                    "endColumnIndex": 3,
                    "startColumnIndex": 0,
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
                    # A1:C4
                    "endRowIndex": 4,
                    "startRowIndex": 0,
                    "endColumnIndex": 3,
                    "startColumnIndex": 0,
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
def conditional_format_custom_condition(conditional_format):
    return [
        *conditional_format,
        {
            "ranges": [
                {
                    "sheetId": "Sheet1",
                    # A1:C4
                    "endRowIndex": 4,
                    "startRowIndex": 0,
                    "endColumnIndex": 3,
                    "startColumnIndex": 0,
                }
            ],
            "booleanRule": {
                "condition": {
                    "type": "CUSTOM_FORMULA",
                    "values": [{"userEnteredValue": "=SUM(A1:A14) \u003e 50"}],
                },
                "format": {
                    "backgroundColor": {
                        "red": 0.95686275,
                        "green": 0.78039217,
                        "blue": 0.7647059,
                    }
                },
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


@pytest.fixture()
def solution_data_custom_condition(conditional_format_custom_condition):
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
        "conditionalFormats": conditional_format_custom_condition,
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
            compose(
                Deletion(["conditionalFormats", 0, "booleanRule"]),
                Mutation(["conditionalFormats", 0, "gradientRule"], {}),
            ),
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
            compose(
                Deletion(["conditionalFormats", 1, "gradientRule"]),
                Mutation(["conditionalFormats", 1, "booleanRule"], {}),
            ),
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


@pytest.mark.parametrize(
    "trans, correct, match",
    [(Deletion(["conditionalFormats", 1]), False, "enough conditional format rules")],
)
def test_has_equal_conditional_formats_3(solution_data_2, trans, correct, match):
    user_data = trans(deepcopy(solution_data_2))
    # sct_range is irrelevant in conditional formats
    s = setup_state(user_data, solution_data_2, "A1")
    with verify_success(correct, match=match):
        has_equal_conditional_formats(s)


@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (
            Mutation(
                [
                    "conditionalFormats",
                    1,
                    "booleanRule",
                    "condition",
                    "values",
                    0,
                    "userEnteredValue",
                ],
                "=sum(A1:A14) \u003e 50",
            ),
            True,
            None,
        ),
        (
            Mutation(
                [
                    "conditionalFormats",
                    1,
                    "booleanRule",
                    "condition",
                    "values",
                    0,
                    "userEnteredValue",
                ],
                "=SUM(A1:A14)  \u003e 50",
            ),
            True,
            None,
        ),
    ],
)
def test_has_equal_conditional_formats_custom_condition(
    solution_data_custom_condition, trans, correct, match
):
    user_data = trans(deepcopy(solution_data_custom_condition))
    # sct_range is irrelevant in conditional formats
    s = setup_state(user_data, solution_data_custom_condition, "A1")
    with verify_success(correct, match=match):
        has_equal_conditional_formats(s)


def test_has_equal_conditional_formats_fail(solution_data):
    user_data = deepcopy(solution_data)
    user_data["conditionalFormats"][0]["ranges"] = [
        {
            "sheetId": "Sheet1",
            # A1:C5
            "endRowIndex": 5,
            "startRowIndex": 0,
            "endColumnIndex": 3,
            "startColumnIndex": 0,
        }
    ]
    Ex = setup_ex_state(user_data, solution_data, "A1")
    with verify_success(True):
        Ex.has_equal_conditional_formats()


def test_has_equal_conditional_formats_out_of_range(solution_data):
    user_data = deepcopy(solution_data)
    user_data["conditionalFormats"][0]["booleanRule"] = {}
    Ex = setup_ex_state(user_data, solution_data, "Z1")
    with verify_success(True):
        Ex.has_equal_conditional_formats()
