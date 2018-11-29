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

from sheetwhat.checks import has_equal_chart

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
@pytest.mark.parametrize(
    "trans, correct",
    [
        (Identity(), True),
        (Mutation(["charts"], []), False),
        (Mutation(["charts", 0, "spec", "basicChart", "chartType"], "LINE"), False),
        (Mutation(["charts", 0, "spec", "title"], "Other title"), False),
        (Deletion(["charts", 0, "spec", "title"]), False),
        (Mutation(["charts", 0, "spec", "subTitle"], "something"), False),
        (Deletion(["charts", 0, "spec", "basicChart", "domains", 0]), False),
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
        ),
        (Deletion(["charts", 0, "spec", "basicChart", "series", 0]), False),
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
        ),
    ],
)
def test_has_equal_chart(solution_data, trans, correct):
    user_data = trans(deepcopy(solution_data))
    # sct_range is irrelevant in charts
    s = setup_state(user_data, solution_data, "E1")
    with verify_success(correct):
        has_equal_chart(s)


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
                                        "sheetId": 1964080503,
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
    # sct_range is irrelevant in charts
    s = setup_state(user_data, solution_data, "E1")
    with verify_success(correct):
        has_equal_chart(s)


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
                                        "sheetId": 1964080503,
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
    # sct_range is irrelevant in charts
    s = setup_state(user_data, solution_data, "A1")
    with verify_success(correct):
        has_equal_chart(s)
