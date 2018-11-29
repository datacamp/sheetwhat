import functools
from ..utils import range_to_row_columns
from .rules import rule_types, safe_glom


def infer_chart_type(chart):
    chart_types = [
        "basicChart",
        "pieChart",
        "bubbleChart",
        "candlestickChart",
        "orgChart",
        "histogramChart",
        "waterfallChart",
        "treemapChart",
    ]
    for chart_type in chart_types:
        if safe_glom(chart, f"spec.{chart_type}") is not None:
            return chart_type


def manhatten_distance_to_chart(chart, sct_range):
    anchor_cell = safe_glom(chart, "position.overlayPosition.anchorCell")
    x = safe_glom(anchor_cell, "columnIndex", 0)
    y = safe_glom(anchor_cell, "rowIndex", 0)
    sct_range_as_row_columns = range_to_row_columns(sct_range)
    x_sct = safe_glom(sct_range_as_row_columns, "start_column", 0)
    y_sct = safe_glom(sct_range_as_row_columns, "start_row", 0)
    return abs(x - x_sct) + abs(y - y_sct)


def find_chart(charts, sct_range):
    distance_to_sct = functools.partial(
        manhatten_distance_to_chart, sct_range=sct_range
    )
    distances = [distance_to_sct(chart) for chart in charts]
    min_distance_index = distances.index(min(distances))
    return charts[min_distance_index]


def has_equal_chart(state, extra_msg=None):
    solution_chart = find_chart(state.solution_data["charts"], state.sct_range)
    if len(state.student_data["charts"]) == 0:
        state.do_test(f"Please create a chart near `{state.sct_range}`.")
    student_chart = find_chart(state.student_data["charts"], state.sct_range)
    issues = []
    bound_rules = {
        key: RuleClass(student_chart, solution_chart, issues)
        for key, RuleClass in rule_types.items()
    }
    bound_rules["equality"]("spec.title", "The title is not correct."),
    bound_rules["equality"]("spec.subTitle", "The subtitle is not correct.")

    # Figure out chart type
    solution_chart_type = infer_chart_type(solution_chart)

    bound_rules["existence"](
        f"spec.{solution_chart_type}", "The chart type is not correct."
    )

    if solution_chart_type == "basicChart":
        bound_rules["equality"](
            "spec.basicChart.chartType", "The chart type is not correct."
        )

    if len(issues) == 0:
        bound_rules["equality"](
            f"spec.{solution_chart_type}.domains", "The X-axis is not correct."
        )

        bound_rules["array_equal_length"](
            f"spec.{solution_chart_type}.series",
            (
                "The number of series is incorrect. "
                "Expected {expected}, but got {actual}."
            ),
        )
        bound_rules["array_equality"](
            f"spec.{solution_chart_type}.series", ("The {ordinal} series is incorrect.")
        )

    nb_issues = len(issues)
    if nb_issues > 0:
        _issues_msg = "\n".join([f"- {issue}" for issue in issues])
        _msg = (
            f"There {'are' if nb_issues > 1 else 'is'} {nb_issues} "
            f"issue{'s' if nb_issues > 1 else ''} with the chart "
            f"close to `{state.sct_range}`:\n\n{_issues_msg}\n"
        )
        state.do_test(_msg)
