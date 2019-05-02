from functools import partial
from protowhat import selectors

from sheetwhat.selectors import state_selector, Dispatcher
from ..utils import range_to_row_columns, row_columns_to_range
from ..Range import Range
from sheetwhat.Test import EqualityTest, ArrayEqualLengthTest, array_element_tests


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
        if Dispatcher().select(f"spec.{chart_type}", chart) is not None:
            return chart_type


def find_chart_anchor(chart):
    raw_row_columns = Dispatcher().select("position.overlayPosition.anchorCell", chart)
    return {
        "start_row": Dispatcher().select("rowIndex", raw_row_columns, fallback=0),
        "start_column": Dispatcher().select("columnIndex", raw_row_columns, fallback=0),
    }


def manhattan_distance_to_chart(chart, sct_range):
    anchor_cell = find_chart_anchor(chart)
    x = anchor_cell["start_column"]
    y = anchor_cell["start_row"]
    sct_range_as_row_columns = range_to_row_columns(sct_range)
    x_sct = Dispatcher().select("start_column", sct_range_as_row_columns, fallback=0)
    y_sct = Dispatcher().select("start_row", sct_range_as_row_columns, fallback=0)
    return abs(x - x_sct) + abs(y - y_sct)


def find_chart(charts, sct_range):
    distance_to_sct = partial(manhattan_distance_to_chart, sct_range=sct_range)
    distances = [distance_to_sct(chart) for chart in charts]
    min_distance_index = distances.index(min(distances))
    return charts[min_distance_index]


def check_chart(state, extra_msg=None):
    solution_chart = find_chart(state.solution_data["charts"], state.sct_range)
    if len(state.student_data["charts"]) == 0:
        state.report(f"Please create a chart near `{state.sct_range}`.")
    student_chart = find_chart(state.student_data["charts"], state.sct_range)
    student_chart_anchor = row_columns_to_range(find_chart_anchor(student_chart))

    solution_chart_type = infer_chart_type(solution_chart)

    chart_type_msg = (
        f"The chart type of the chart at `{student_chart_anchor}` is not correct."
    )

    if Dispatcher().select(f"spec.{solution_chart_type}", student_chart) is None:
        state.report(chart_type_msg)
    elif solution_chart_type == "basicChart":
        chart_type_path = "spec.basicChart.chartType"
        student_chart_type = Dispatcher().select(chart_type_path, student_chart)
        detailed_solution_chart_type = Dispatcher().select(
            chart_type_path, solution_chart
        )
        if student_chart_type != detailed_solution_chart_type:
            state.report(chart_type_msg)

    return state.to_child(
        student_data=student_chart["spec"],
        solution_data=solution_chart["spec"],
        append_message=f"In the chart at `{student_chart_anchor}`, ",
        node_name=solution_chart_type,
    )


def has_equal_title(state):
    selector = state_selector(state)
    state.do_tests(
        [
            EqualityTest(*selector("title"), "the title is not correct."),
            EqualityTest(*selector("subtitle"), "the subtitle is not correct."),
        ]
    )
    return state


def has_equal_domain(state):
    domain_path = {"basicChart": "basicChart.domains.0.domain.sourceRange.sources.0"}
    if state.node_name in domain_path:
        state.do_test(
            EqualityTest(
                *state_selector(state)(domain_path[state.node_name]),
                "the X-axis is not correct.",
            )
        )
    return state


# todo: make/use Test class
def equal_sources(student_sources, _solution_sources, min_range):
    return any(min_range.is_within(Range(source)) for source in student_sources)


def has_equal_single_series(state, number, min_range_str, series_type):
    base_path = f"basicChart.series.{number - 1}"
    min_range = Range(min_range_str)
    series_path = {
        "basicChart": {
            "source": f"{base_path}.series.sourceRange.sources",
            "color": f"{base_path}.color",
        }
    }
    series_equality = {"source": partial(equal_sources, min_range=min_range)}
    ordinal = selectors.get_ord(number)
    if state.node_name in series_path:
        state.do_test(
            EqualityTest(
                *state_selector(state)(series_path[state.node_name].get(series_type)),
                f"the {ordinal} series' {series_type} is not correct.",
                series_equality.get(series_type, lambda x, y: x == y),
            )
        )
    return state


def has_equal_series(state):
    series_path = {
        "basicChart": {
            "source": ("basicChart.series", ["series.sourceRange.sources"]),
            "color": ("basicChart.series", ["color"]),
        }
    }
    if state.node_name in series_path:
        selector = state_selector(state)

        state.do_tests(
            array_element_tests(
                EqualityTest,
                *selector(series_path[state.node_name].get("source")),
                state.build_message("the {ordinal} series' source is not correct."),
            )
            + array_element_tests(
                EqualityTest,
                *selector(series_path[state.node_name].get("color")),
                state.build_message("the {ordinal} series' color is not correct."),
            )
        )
    return state


def has_equal_node(state, test, path, message):
    test_classes = {
        "equality": EqualityTest,
        "array_equal_length": ArrayEqualLengthTest,
        "array_equality": partial(array_element_tests, EqualityTest),
    }
    tests = test_classes.get(test)(*state_selector(state)(path), message)
    if not isinstance(tests, list):
        tests = [tests]
    state.do_tests(tests)
    return state
