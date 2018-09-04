# import pytest
# from copy import deepcopy
# from helper import Identity, Mutation, setup_state, verify_success, compose, Deletion, Addition
#
## Fixtures
# @pytest.fixture()
# def charts():
#    return [
#        {
#            "chartId": 873985484,
#            "spec": {
#                "title": "Adams, Baker, Clark and Davis",
#                "basicChart": {
#                    "chartType": "AREA",
#                    "legendPosition": "RIGHT_LEGEND",
#                    "axis": [
#                        {
#                            "position": "BOTTOM_AXIS",
#                            "title": "Day",
#                            "format": {"fontFamily": "Roboto"},
#                        },
#                        {"position": "LEFT_AXIS"},
#                    ],
#                    "domains": [
#                        {
#                            "domain": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 0,
#                                            "endColumnIndex": 1,
#                                        }
#                                    ]
#                                }
#                            }
#                        }
#                    ],
#                    "series": [
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 1,
#                                            "endColumnIndex": 2,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 2,
#                                            "endColumnIndex": 3,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 3,
#                                            "endColumnIndex": 4,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 4,
#                                            "endColumnIndex": 5,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                    ],
#                    "headerCount": 1,
#                    "stackedType": "STACKED",
#                },
#                "hiddenDimensionStrategy": "SKIP_HIDDEN_ROWS_AND_COLUMNS",
#                "titleTextFormat": {"fontFamily": "Roboto"},
#                "fontName": "Roboto",
#            },
#            "position": {
#                "overlayPosition": {
#                    "anchorCell": {"sheetId": "Sheet1", "columnIndex": 6},
#                    "offsetXPixels": 3,
#                    "widthPixels": 600,
#                    "heightPixels": 371,
#                }
#            },
#        },
#        {
#            "chartId": 1653050700,
#            "spec": {
#                "basicChart": {
#                    "chartType": "COLUMN",
#                    "legendPosition": "RIGHT_LEGEND",
#                    "axis": [{"position": "BOTTOM_AXIS"}, {"position": "LEFT_AXIS"}],
#                    "domains": [
#                        {
#                            "domain": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 0,
#                                            "endColumnIndex": 1,
#                                        }
#                                    ]
#                                }
#                            }
#                        }
#                    ],
#                    "series": [
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 1,
#                                            "endColumnIndex": 2,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 2,
#                                            "endColumnIndex": 3,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 3,
#                                            "endColumnIndex": 4,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                        {
#                            "series": {
#                                "sourceRange": {
#                                    "sources": [
#                                        {
#                                            "startRowIndex": 0,
#                                            "endRowIndex": 8,
#                                            "startColumnIndex": 4,
#                                            "endColumnIndex": 5,
#                                        }
#                                    ]
#                                }
#                            },
#                            "targetAxis": "LEFT_AXIS",
#                        },
#                    ],
#                },
#                "hiddenDimensionStrategy": "SKIP_HIDDEN_ROWS_AND_COLUMNS",
#                "fontName": "Roboto",
#            },
#            "position": {
#                "overlayPosition": {
#                    "anchorCell": {"sheetId": "Sheet1"},
#                    "widthPixels": 600,
#                    "heightPixels": 371,
#                }
#            },
#        },
#    ]
#
#
# @pytest.fixture()
# def solution_data(charts):
#    return {
#        "values": [[1, 1, 1], [1, 52, 8]],
#        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
#        "charts": charts,
#    }
#
#
## Tests
# @pytest.mark.parametrize(
#    "trans, sct_range, correct",
#    [
#        (Identity(), "A1", True),
#        (
#            Mutation(["charts", 0, "spec", "basicChart", "chartType"], "LINE"),
#            "A1",
#            False,
#        ),
#        (
#            Mutation(["charts", 1, "spec", "basicChart", "chartType"], "LINE"),
#            "A1",
#            True,
#        ),
#        (Mutation(["charts", 0, "spec", "title"], "Other title"), "A1", False),
#        (Deletion(["charts", 0, "spec", "title"]), "A1", False),
#        (Mutation(["charts", 0, "spec", "subTitle"], "something"), "A1", False),
#    ],
# )
# def test_check_charts(solution_data, trans, sct_range, correct):
#    user_data = trans(deepcopy(solution_data))
#    s = setup_state(user_data, solution_data)
#    with verify_success(correct):
#       has_equal_chart(s)
