import pytest
from copy import deepcopy
from tests.helper import (
    Identity,
    Mutation,
    setup_state,
    verify_success,
    compose,
    Deletion,
    Addition,
)
from sheetwhat.checks import has_equal_pivot

# Fixtures
@pytest.fixture()
def pivot_tables():
    return [
        [
            {
                "source": {
                    "startRowIndex": 0,
                    "endRowIndex": 613,
                    "startColumnIndex": 0,
                    "endColumnIndex": 5,
                },
                "rows": [{"showTotals": True, "sortOrder": "ASCENDING"}],
                "columns": [
                    {
                        "sourceColumnOffset": 2,
                        "showTotals": True,
                        "sortOrder": "ASCENDING",
                    }
                ],
                "values": [
                    {
                        "sourceColumnOffset": 4,
                        "summarizeFunction": "SUM",
                        "calculatedDisplayType": "PERCENT_OF_ROW_TOTAL",
                    }
                ],
                "criteria": {
                    "0": {
                        "visibleValues": [
                            "01-Jan",
                            "02-Feb",
                            "03-Mar",
                            "04-Apr",
                            "05-May",
                            "06-Jun",
                            "07-Jul",
                            "08-Aug",
                            "09-Sep",
                            "10-Oct",
                        ]
                    }
                },
            }
        ]
    ]


@pytest.fixture()
def pivot_tables_two_values():
    return [
        [
            {
                "source": {
                    "startRowIndex": 0,
                    "endRowIndex": 613,
                    "startColumnIndex": 0,
                    "endColumnIndex": 5,
                },
                "rows": [],
                "values": [
                    {"sourceColumnOffset": 3, "summarizeFunction": "MAX"},
                    {"sourceColumnOffset": 4, "summarizeFunction": "MAX"},
                ],
                "criteria": {
                    "0": {
                        "visibleValues": [
                            "01-Jan",
                            "02-Feb",
                            "03-Mar",
                            "04-Apr",
                            "05-May",
                            "06-Jun",
                            "07-Jul",
                            "08-Aug",
                            "09-Sep",
                            "10-Oct",
                        ]
                    }
                },
            }
        ]
    ]


@pytest.fixture()
def solution_data(pivot_tables):
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
        "pivotTables": pivot_tables,
    }


@pytest.fixture()
def solution_data_two_values(pivot_tables_two_values):
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
        "pivotTables": pivot_tables_two_values,
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, correct, message_contains",
    [
        (Identity(), "A1", True, None),
        (
            Mutation(["pivotTables", 0, 0, "source", "startRowIndex"], 1),
            "A1",
            False,
            r"1 issue(.|\s)*source data",
        ),
        (
            Mutation(["pivotTables", 0, 0, "source", "endRowIndex"], 1),
            "A1",
            False,
            r"1 issue(.|\s)*source data",
        ),
        (
            Mutation(["pivotTables", 0, 0, "source", "startColumnIndex"], 1),
            "A1",
            False,
            r"1 issue(.|\s)*source data",
        ),
        (
            Mutation(["pivotTables", 0, 0, "source", "endColumnIndex"], 1),
            "A1",
            False,
            r"1 issue(.|\s)*source data",
        ),
        (
            Mutation(["pivotTables", 0, 0, "source", "startRowIndex"], 1),
            "B1",
            False,
            r"fill in(.|\s)*pivot table(.|\s)*`B1`",
        ),
        (
            Mutation(["pivotTables", 0, 0, "rows", 0, "sortOrder"], "DESCENDING"),
            "A1",
            False,
            r"1 issue(.|\s)*sort order",
        ),
        (
            Deletion(["pivotTables", 0, 0, "rows"]),
            "A1",
            False,
            r"1 issue(.|\s)*There are no rows",
        ),
        (
            Deletion(["pivotTables", 0, 0, "columns"]),
            "A1",
            False,
            r"1 issue(.|\s)*There are no columns",
        ),
        (
            Deletion(["pivotTables", 0, 0, "values"]),
            "A1",
            False,
            r"1 issue(.|\s)*There are no values",
        ),
        (
            Deletion(["pivotTables", 0, 0, "criteria"]),
            "A1",
            False,
            r"1 issue(.|\s)*There are no filters",
        ),
        (
            Mutation(
                ["pivotTables", 0, 0, "columns", 0, "valueBucket"],
                {"buckets": [{"stringValue": "01-Jan"}]},
            ),
            "A1",
            False,
            r"1 issue(.|\s)*sort group",
        ),
        (
            Mutation(["pivotTables", 0, 0, "columns", 0, "sourceColumnOffset"], 1),
            "A1",
            False,
            r"1 issue(.|\s)*column(.|\s)*grouping variable(.|\s)*incorrect",
        ),
        (
            Mutation(
                ["pivotTables", 0, 0, "values", 0, "summarizeFunction"], "AVERAGE"
            ),
            "A1",
            False,
            r"1 issue(.|\s)*expected the first(.|\s)*`SUM`, but got `AVERAGE`",
        ),
        (
            Deletion(["pivotTables", 0, 0, "columns", 0, "showTotals"]),
            "A1",
            False,
            r"1 issue(.|\s)*first(.|\s)*total(.|\s)*not showing",
        ),
        (
            Deletion(["pivotTables", 0, 0, "values", 0, "calculatedDisplayType"]),
            "A1",
            False,
            # TODO: message?
            None,
        ),
        (
            Addition(
                ["pivotTables", 0, 0, "rows"],
                {"showTotals": True, "sortOrder": "ASCENDING"},
            ),
            "A1",
            False,
            r"1 issue(.|\s)*The number of rows is incorrect",
        ),
    ],
)
def test_check_pivots(solution_data, trans, sct_range, correct, message_contains):
    user_data = trans(deepcopy(solution_data))
    s = setup_state(user_data, solution_data, sct_range)
    with verify_success(correct, message_contains):
        has_equal_pivot(s)


@pytest.mark.parametrize(
    "trans, sct_range, correct, message_contains",
    [
        (Identity(), "A1", True, None),
        (
            Deletion(["pivotTables", 0, 0, "values", 1]),
            "A1",
            False,
            r"1 issue(.|\s)*The number of values is incorrect",
        ),
        (
            Addition(
                ["pivotTables", 0, 0, "rows"],
                {"showTotals": True, "sortOrder": "ASCENDING"},
            ),
            "A1",
            False,
            r"1 issue(.|\s)*There are rows but there shouldn't be",
        ),
        (
            Mutation(
                ["pivotTables", 0, 0, "columns"],
                [{"showTotals": True, "sortOrder": "ASCENDING"}],
            ),
            "A1",
            False,
            r"1 issue(.|\s)*There are columns(.|\s)*shouldn't be",
        ),
    ],
)
def test_check_pivots_two_values(
    solution_data_two_values, trans, sct_range, correct, message_contains
):
    user_data = trans(deepcopy(solution_data_two_values))
    s = setup_state(user_data, solution_data_two_values, sct_range)
    with verify_success(correct, message_contains):
        has_equal_pivot(s)
