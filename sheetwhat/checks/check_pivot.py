from sheetwhat.checks import check_range
from sheetwhat.utils import dict_keys, normalize_formula

from .rules import rule_types, safe_glom


def has_equal_pivot(state, extra_msg=None):
    child = check_range(state, field="pivotTables", field_msg="pivot table")

    student_pivot_tables = child.student_data["pivotTables"]
    solution_pivot_tables = child.solution_data["pivotTables"]

    for i, student_row in enumerate(student_pivot_tables):
        for j, student_pivot_table in enumerate(student_row):
            solution_pivot_table = solution_pivot_tables[i][j]
            issues = []
            bound_rules = {
                key: RuleClass(student_pivot_table, solution_pivot_table, issues)
                for key, RuleClass in rule_types.items()
            }

            bound_rules["existence"]("rows", "There are no rows."),
            bound_rules["existence"]("columns", "There are no columns.")
            bound_rules["existence"]("values", "There are no values.")
            bound_rules["existence"]("criteria", "There are no filters.")
            bound_rules["over_existence"](
                "rows", "There are rows but there shouldn't be."
            ),
            bound_rules["over_existence"](
                "columns", "There are columns but there shouldn't be."
            )
            bound_rules["over_existence"](
                "values", "There are values but there shouldn't be."
            )
            bound_rules["equality"]("source", "The source data is incorrect.")
            bound_rules["array_equality"](
                ("rows", ["sortOrder"]),
                (
                    "Inside rows, expected the {ordinal} sort order to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            bound_rules["array_equality"](
                ("columns", ["sortOrder"]),
                (
                    "Inside columns, expected the {ordinal} sort order to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            bound_rules["array_equality"](
                ("rows", ["valueBucket"]),
                (
                    "Inside rows, expected the {ordinal} sort group to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            bound_rules["array_equality"](
                ("columns", ["valueBucket"]),
                (
                    "Inside columns, expected the {ordinal} sort group to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            bound_rules["array_equality"](
                ("rows", ["sourceColumnOffset"]),
                ("Inside rows, the {ordinal} grouping variable is incorrect."),
            )
            bound_rules["array_equality"](
                ("columns", ["sourceColumnOffset"]),
                ("Inside columns, the {ordinal} grouping variable is incorrect."),
            )
            bound_rules["array_equality"](
                ("rows", ["showTotals"]),
                ("Inside rows, the {ordinal} totals are not showing."),
            )
            bound_rules["array_equality"](
                ("columns", ["showTotals"]),
                ("Inside columns, the {ordinal} totals are not showing."),
            )
            bound_rules["array_equality"](
                ("values", ["summarizeFunction"]),
                (
                    "Inside values, expected the {ordinal} summarize function "
                    "to be `{expected}`, but got `{actual}`."
                ),
            )
            bound_rules["array_equality"](
                ("values", ["calculatedDisplayType"]),
                (
                    "Inside values, expected the {ordinal} display type "
                    "to be `{expected}`, but got `{actual}`."
                ),
            )
            bound_rules["array_equal_length"](
                "values",
                (
                    "The number of values is incorrect. "
                    "Expected {expected}, but got {actual}."
                ),
            )
            bound_rules["array_equal_length"](
                "rows",
                (
                    "The number of rows is incorrect. "
                    "Expected {expected}, but got {actual}."
                ),
            )
            bound_rules["array_equal_length"](
                "columns",
                (
                    "The number of columns is incorrect. "
                    "Expected {expected}, but got {actual}."
                ),
            )

            bound_rules["dict_key_equality"](
                "criteria", "The rows or columns used in the filter are incorrect."
            )
            for key in dict_keys(
                safe_glom(solution_pivot_table, "criteria"),
                safe_glom(student_pivot_table, "criteria"),
            ):
                bound_rules["set_equality"](
                    f"criteria.{key}.visibleValues",
                    "The filtered out values are incorrect.",
                )

            bound_rules["array_equality"](
                ("values", ["formula"]),
                "The {ordinal} value does not contain the correct calculated field.",
                lambda x, y: normalize_formula(x) == normalize_formula(y),
            )

            nb_issues = len(issues)
            if nb_issues > 0:
                _issues_msg = "\n".join([f"- {issue}" for issue in issues])
                _msg = (
                    f"There {'are' if nb_issues > 1 else 'is'} {nb_issues} "
                    f"issue{'s' if nb_issues > 1 else ''} with the pivot table "
                    f"at `{child.sct_range}`:\n\n{_issues_msg}\n"
                )
                child.do_test(_msg)


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


def has_equal_chart(state, extra_msg=None):
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
