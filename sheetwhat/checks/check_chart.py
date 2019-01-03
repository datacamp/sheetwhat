import functools
from protowhat import selectors

from ..utils import range_to_row_columns, row_columns_to_range
from ..Range import Range
from .rules import with_rules, safe_glom


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


def find_chart_anchor(chart):
    raw_row_columns = safe_glom(chart, "position.overlayPosition.anchorCell")
    return {
        "start_row": safe_glom(raw_row_columns, "rowIndex", 0),
        "start_column": safe_glom(raw_row_columns, "columnIndex", 0),
    }


def manhatten_distance_to_chart(chart, sct_range):
    anchor_cell = find_chart_anchor(chart)
    x = anchor_cell["start_column"]
    y = anchor_cell["start_row"]
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


def check_chart(state, extra_msg=None):
    solution_chart = find_chart(state.solution_data["charts"], state.sct_range)
    if len(state.student_data["charts"]) == 0:
        state.do_test(f"Please create a chart near `{state.sct_range}`.")
    student_chart = find_chart(state.student_data["charts"], state.sct_range)
    student_chart_anchor = row_columns_to_range(find_chart_anchor(student_chart))

    solution_chart_type = infer_chart_type(solution_chart)

    chart_type_msg = (
        f"The chart type of the chart at `{student_chart_anchor}` is not correct."
    )

    if safe_glom(student_chart, f"spec.{solution_chart_type}") is None:
        state.do_test(chart_type_msg)
    elif solution_chart_type == "basicChart":
        chart_type_path = "spec.basicChart.chartType"
        student_chart_type = safe_glom(student_chart, chart_type_path)
        detailed_solution_chart_type = safe_glom(solution_chart, chart_type_path)
        if student_chart_type != detailed_solution_chart_type:
            state.do_test(chart_type_msg)

    state.set_root_message(f"in the chart at `{student_chart_anchor}`")

    return state.to_child(
        student_data=student_chart["spec"],
        solution_data=solution_chart["spec"],
        node_name=solution_chart_type,
    )


@with_rules
def has_equal_title(state, rules):
    rules["equality"]("title", "the title is not correct"),
    rules["equality"]("subtitle", "the subtitle is not correct")
    return state


@with_rules
def has_equal_domain(state, rules):
    domain_path = {"basicChart": "basicChart.domains.0.domain.sourceRange.sources.0"}
    if state.node_name in domain_path:
        rules["equality"](domain_path[state.node_name], "the X-axis is not correct")
    return state


def equal_sources(student_sources, _solution_sources, min_range):
    return any(min_range.is_within(Range(source)) for source in student_sources)


@with_rules
def has_equal_single_series(state, number, min_range_str, series_type, rules):
    base_path = f"basicChart.series.{number - 1}"
    min_range = Range(min_range_str)
    series_path = {
        "basicChart": {
            "source": f"{base_path}.series.sourceRange.sources",
            "color": f"{base_path}.color",
        }
    }
    series_equality = {"source": functools.partial(equal_sources, min_range=min_range)}
    ordinal = selectors.get_ord(number)
    if state.node_name in series_path:
        rules["equality"](
            series_path[state.node_name].get(series_type),
            f"the {ordinal} series' {series_type} is not correct",
            series_equality.get(series_type, lambda x, y: x == y),
        )
    return state


@with_rules
def has_equal_series(state, rules):
    series_path = {
        "basicChart": {
            "source": ("basicChart.series", ["series.sourceRange.sources"]),
            "color": ("basicChart.series", ["color"]),
        }
    }
    if state.node_name in series_path:
        rules["array_equality"](
            series_path[state.node_name].get("source"),
            "the {ordinal} series' source is not correct",
        )
        rules["array_equality"](
            series_path[state.node_name].get("color"),
            "the {ordinal} series' color is not correct",
        )
    return state


@with_rules
def has_equal_node(state, rule, path, message, rules):
    rule = rules.get(rule)
    if callable(rule):
        rule(path, message)
    return state
