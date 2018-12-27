import pytest
from copy import deepcopy
from tests.helper import (
    Identity,
    Mutation,
    setup_state,
    setup_ex_state,
    verify_success,
    compose,
    Deletion,
    Addition,
)

from sheetwhat.checks import check_chart

# Fixtures
@pytest.fixture()
def charts():
    return [
        {
            "chartId": 873985484,
            "spec": {
                "title": "Adams, Baker, Clark and Davis",
                "basicChart": {
                    "chartType": "AREA",
                    "legendPosition": "RIGHT_LEGEND",
                    "axis": [
                        {
                            "position": "BOTTOM_AXIS",
                            "title": "Day",
                            "format": {"fontFamily": "Roboto"},
                        },
                        {"position": "LEFT_AXIS"},
                    ],
                    "domains": [
                        {
                            "domain": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 0,
                                            "endColumnIndex": 1,
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "series": [
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 1,
                                            "endColumnIndex": 2,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 2,
                                            "endColumnIndex": 3,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 3,
                                            "endColumnIndex": 4,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 4,
                                            "endColumnIndex": 5,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                    ],
                    "headerCount": 1,
                    "stackedType": "STACKED",
                },
                "hiddenDimensionStrategy": "SKIP_HIDDEN_ROWS_AND_COLUMNS",
                "titleTextFormat": {"fontFamily": "Roboto"},
                "fontName": "Roboto",
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": "Sheet1", "columnIndex": 6},
                    "offsetXPixels": 3,
                    "widthPixels": 600,
                    "heightPixels": 371,
                }
            },
        },
        {
            "chartId": 1653050700,
            "spec": {
                "basicChart": {
                    "chartType": "COLUMN",
                    "legendPosition": "RIGHT_LEGEND",
                    "axis": [{"position": "BOTTOM_AXIS"}, {"position": "LEFT_AXIS"}],
                    "domains": [
                        {
                            "domain": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 0,
                                            "endColumnIndex": 1,
                                        }
                                    ]
                                }
                            }
                        }
                    ],
                    "series": [
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 1,
                                            "endColumnIndex": 2,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 2,
                                            "endColumnIndex": 3,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 3,
                                            "endColumnIndex": 4,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                        {
                            "series": {
                                "sourceRange": {
                                    "sources": [
                                        {
                                            "sheetId": "Sheet1",
                                            "startRowIndex": 0,
                                            "endRowIndex": 8,
                                            "startColumnIndex": 4,
                                            "endColumnIndex": 5,
                                        }
                                    ]
                                }
                            },
                            "targetAxis": "LEFT_AXIS",
                        },
                    ],
                },
                "hiddenDimensionStrategy": "SKIP_HIDDEN_ROWS_AND_COLUMNS",
                "fontName": "Roboto",
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {"sheetId": "Sheet1"},
                    "widthPixels": 600,
                    "heightPixels": 371,
                }
            },
        },
    ]


@pytest.fixture()
def solution_data(charts):
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
        "charts": charts,
    }


# Tests

## check_chart
@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (Mutation(["charts"], []), False, "Please create a chart near `E1`."),
        (
            Mutation(["charts", 0, "spec", "basicChart", "chartType"], "LINE"),
            False,
            "The chart type .* is not correct",
        ),
        (Mutation(["charts", 0, "spec", "title"], "Other title"), True, None),
        (Mutation(["charts", 0, "spec", "subtitle"], "Other title"), True, None),
    ],
)
def test_check_chart(solution_data, trans, correct, match):
    solution_data = deepcopy(solution_data)
    student_data = trans(deepcopy(solution_data))

    s = setup_ex_state(student_data, solution_data, "E1")
    with verify_success(correct, match=match):
        s.check_chart()


## has_equal_title
@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (Mutation(["charts", 0, "spec", "title"], "Other title"), False, None),
        (Mutation(["charts", 0, "spec", "subtitle"], "Other title"), False, None),
        (
            Mutation(["charts", 0, "spec", "title"], "Other title"),
            False,
            "title .* not correct",
        ),
        (Deletion(["charts", 0, "spec", "title"]), False, "title .* not correct"),
        (
            Mutation(["charts", 0, "spec", "subtitle"], "test"),
            False,
            "subtitle .* not correct",
        ),
    ],
)
def test_has_equal_title(solution_data, trans, correct, match):
    solution_data = deepcopy(solution_data)
    student_data = trans(deepcopy(solution_data))

    s = setup_ex_state(student_data, solution_data, "E1")
    with verify_success(correct, match=match):
        s.check_chart().has_equal_title()


## has_equal_domain
@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (
            Deletion(["charts", 0, "spec", "basicChart", "domains", 0]),
            False,
            "X-axis .* not correct",
        ),
        (
            Mutation(
                [
                    "charts",
                    0,
                    "spec",
                    "basicChart",
                    "domains",
                    0,
                    "domain",
                    "sourceRange",
                    "sources",
                    0,
                ],
                {
                    "startRowIndex": 1,
                    "endRowIndex": 8,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2,
                },
            ),
            False,
            "X-axis",
        ),
    ],
)
def test_has_equal_domain(solution_data, trans, correct, match):
    solution_data = deepcopy(solution_data)
    student_data = trans(deepcopy(solution_data))

    s = setup_ex_state(student_data, solution_data, "E1")
    with verify_success(correct, match=match):
        s.check_chart().has_equal_domain()


## has_equal_series
@pytest.mark.parametrize(
    "trans, correct, match",
    [
        (Identity(), True, None),
        (Deletion(["charts", 0, "spec", "basicChart", "series", 0]), False, None),
        (
            Addition(
                [
                    "charts",
                    0,
                    "spec",
                    "basicChart",
                    "series",
                    0,
                    "series",
                    "sourceRange",
                    "sources",
                ],
                {
                    "startRowIndex": 1,
                    "endRowIndex": 8,
                    "startColumnIndex": 5,
                    "endColumnIndex": 6,
                },
            ),
            False,
            "In the chart at .*, the first serie's source is not correct",
        ),
        (
            Mutation(
                [
                    "charts",
                    0,
                    "spec",
                    "basicChart",
                    "series",
                    0,
                    "series",
                    "sourceRange",
                    "sources",
                    0,
                ],
                {
                    "startRowIndex": 1,
                    "endRowIndex": 8,
                    "startColumnIndex": 5,
                    "endColumnIndex": 6,
                },
            ),
            False,
            None,
        ),
    ],
)
def test_has_equal_series(solution_data, trans, correct, match):
    solution_data = deepcopy(solution_data)
    student_data = trans(deepcopy(solution_data))

    s = setup_ex_state(student_data, solution_data, "E1")
    with verify_success(correct, match=match):
        s.check_chart().has_equal_series()


@pytest.mark.parametrize(
    "trans, correct",
    [
        (
            compose(
                Deletion(["charts", 0, "spec", "basicChart"]),
                Mutation(
                    ["charts", 0, "spec", "pieChart"],
                    {
                        "domain": {
                            "sourceRange": {
                                "sources": [
                                    {
                                        "sheetId": "Sheet1",
                                        "startRowIndex": 0,
                                        "endRowIndex": 4,
                                        "startColumnIndex": 0,
                                        "endColumnIndex": 1,
                                    }
                                ]
                            }
                        }
                    },
                ),
            ),
            False,
        )
    ],
)
def test_has_equal_chart_trans_on_solution(solution_data, trans, correct):
    user_data = deepcopy(solution_data)
    solution_data = trans(deepcopy(solution_data))
    s = setup_ex_state(user_data, solution_data, "E1")
    with verify_success(correct):
        s.check_chart()


@pytest.mark.parametrize(
    "trans, correct",
    [
        (Identity(), True),
        (
            compose(
                Deletion(["charts", 0, "spec", "basicChart"]),
                Mutation(
                    ["charts", 0, "spec", "pieChart"],
                    {
                        "domain": {
                            "sourceRange": {
                                "sources": [
                                    {
                                        "sheetId": "Sheet1",
                                        "startRowIndex": 0,
                                        "endRowIndex": 4,
                                        "startColumnIndex": 0,
                                        "endColumnIndex": 1,
                                    }
                                ]
                            }
                        }
                    },
                ),
            ),
            True,
        ),
    ],
)
def test_has_equal_chart_trans_on_other_chart(solution_data, trans, correct):
    user_data = deepcopy(solution_data)
    solution_data = trans(deepcopy(solution_data))
    s = setup_ex_state(user_data, solution_data, "A1")
    with verify_success(correct):
        s.check_chart()
