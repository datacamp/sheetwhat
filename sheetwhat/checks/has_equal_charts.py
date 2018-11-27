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


def has_equal_charts(state, extra_msg=None):
    solution_chart = state.solution_data["charts"][0]
    if len(state.student_data["charts"]) == 0:
        state.do_test("Please create a chart.")
    student_chart = state.student_data["charts"][0]
    issues = []
    bound_rules = {
        key: RuleClass(student_chart, solution_chart, issues)
        for key, RuleClass in rule_types.items()
    }
    bound_rules["existence"]("spec.title", "There is no title."),
    bound_rules["equality"]("spec.title", "The title is not correct."),
    bound_rules["existence"]("spec.subTitle", "There is no subtitle.")
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
        bound_rules["existence"](
            f"spec.{solution_chart_type}.domains", "There is no XYZ specified."
        )
        bound_rules["array_equality"](
            f"spec.{solution_chart_type}.domains", "The {ordinal} XYZ is not correct."
        )
        bound_rules["existence"](
            f"spec.{solution_chart_type}.series", "There are no series specified."
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
            f"issue{'s' if nb_issues > 1 else ''} with the chart:"
            f"\n\n{_issues_msg}\n"
        )
        state.do_test(_msg)
