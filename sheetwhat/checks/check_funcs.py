from .utils import (
    crop_by_range,
    is_empty,
    round_array_2d,
    normalize_array_2d,
    map_2d,
    normalize_formula,
)
import copy
import re
import glom
import functools
from protowhat import selectors


def check_range(state, field, field_msg, missing_msg=None):

    student_field_content = crop_by_range(state.student_data[field], state.sct_range)
    solution_field_content = crop_by_range(state.solution_data[field], state.sct_range)

    if is_empty(student_field_content):
        _msg = missing_msg or f"Please fill in a {field_msg} in `{state.sct_range}`."
        state.do_test(_msg)

    return state.to_child(
        {**copy.deepcopy(state.student_data), field: student_field_content},
        {**copy.deepcopy(state.solution_data), field: solution_field_content},
    )


def has_code(state, pattern, fixed=False, incorrect_msg=None, normalize=lambda x: x):
    child = check_range(state, field="formulas", field_msg="formula")

    def match(on_text):
        if fixed:
            return normalize(pattern) in str(on_text)
        else:
            return re.search(pattern, str(on_text)) is not None

    student_formulas_normalized = map_2d(normalize, child.student_data["formulas"])
    student_matches = map_2d(match, student_formulas_normalized)

    if not all([all(row) for row in student_matches]):
        _msg = (
            incorrect_msg
            or f"In cell `{state.sct_range}`, did you use the correct formula?"
        )
        child.do_test(_msg)

    return state


def check_function(state, name, missing_msg=None):
    missing_msg = (
        missing_msg
        or f"In cell `{state.sct_range}`, did you use the `{name}()` function?"
    )
    has_code(
        state,
        pattern=name,
        fixed=True,
        incorrect_msg=missing_msg,
        normalize=normalize_formula,
    )
    # Don't return state; chaining not implemented yet
    return None


def check_operator(state, operator, missing_msg=None):
    missing_msg = (
        missing_msg
        or f"In cell `{state.sct_range}`, did you use the `{operator}` operator?"
    )
    has_code(
        state,
        pattern=operator,
        fixed=True,
        incorrect_msg=missing_msg,
        normalize=normalize_formula,
    )
    # Don't return state; chaining not implemented yet
    return None


def has_equal_value(state, incorrect_msg=None, ndigits=4):
    child = check_range(state, field="values", field_msg="value")

    student_values_rounded = round_array_2d(child.student_data["values"], ndigits)
    solution_values_rounded = round_array_2d(child.solution_data["values"], ndigits)

    if student_values_rounded != solution_values_rounded:
        _msg = incorrect_msg or f"The value at `{child.sct_range}` is not correct."
        child.do_test(_msg)

    return state


def has_equal_formula(state, incorrect_msg=None, ndigits=4):
    child = check_range(state, field="formulas", field_msg="formula")

    student_formulas_normalized = normalize_array_2d(child.student_data["formulas"])
    solution_formulas_normalized = normalize_array_2d(child.solution_data["formulas"])

    if student_formulas_normalized != solution_formulas_normalized:
        _msg = (
            incorrect_msg
            or f"In cell `{state.sct_range}`, did you use the correct formula?"
        )
        child.do_test(_msg)

    return state


def has_equal_references(state, absolute=False, incorrect_msg=None):
    child = check_range(state, field="formulas", field_msg="formula")

    if absolute:
        pattern = r"\$?[A-Z]+\$?\d+(?:\:\$?[A-Z]+\$?\d+)?"
    else:
        pattern = r"[A-Za-z]+\d+(?:\:[A-Za-z]+\d+)?"

    student_formulas = child.student_data["formulas"]
    solution_formulas = child.solution_data["formulas"]

    for i, student_row in enumerate(student_formulas):
        for j, student_cell in enumerate(student_row):
            solution_cell = str(solution_formulas[i][j])
            student_cell = str(student_cell)
            solution_references = re.findall(pattern, solution_cell)

            for reference in solution_references:
                if normalize_formula(reference) not in normalize_formula(student_cell):
                    _msg = (
                        f"In cell {child.sct_range}, did you use the "
                        f"{('absolute ' if absolute else '')}"
                        f"reference `{reference}`"
                    )
                    child.do_test(_msg)


# Supercharge path with appropriate coalesce at every level
# E.g.
#  deep_coalesce("path", None) => Coalesce("path", default=None)
#  deep_coalesce(("path", ), None) =>
#    Coalesce((Coalesce("path", default=None),), default=None)
# etc. (tuples and lists work analogously)
def deep_coalesce(path, default):
    if isinstance(path, (tuple, list)):
        path = type(path)(deep_coalesce(p, default) for p in path)
    return glom.Coalesce(path, default=default)


def safe_glom(obj, path, fallback=None):
    return glom.glom(obj, deep_coalesce(path, fallback))


class Rule:
    def __init__(self, student_pivot_table, solution_pivot_table, issues):
        self.student_pivot_table = student_pivot_table
        self.solution_pivot_table = solution_pivot_table
        self.issues = issues

class ArrayEqualityRule(Rule):
    def __call__(self, path, message):
        solution_array = safe_glom(self.solution_pivot_table, path)
        student_array = safe_glom(self.student_pivot_table, path)
        if not isinstance(student_array, list):
            return
        if not isinstance(solution_array, list):
            return
        if solution_array != student_array:
            matches = [x == y for x, y in zip(student_array, solution_array)]
            mismatch_reducer = lambda all, x: all if x[1] else [*all, x[0]]
            mismatch_indices = functools.reduce(
                mismatch_reducer, enumerate(matches), []
            )

            self.issues.extend(
                [
                    message.format(
                        ordinal=selectors.get_ord(i + 1),
                        expected=solution_array[i],
                        actual=student_array[i],
                    )
                    for i in mismatch_indices
                ]
            )

class ArrayEqualLengthRule(Rule):
    def __call__(self, path, message):
        solution_array = safe_glom(self.solution_pivot_table, path)
        student_array = safe_glom(self.student_pivot_table, path)
        if not isinstance(student_array, list):
            return
        if not isinstance(solution_array, list) or len(solution_array) == 0:
            return
        solution_array_len = len(solution_array)
        student_array_len = len(student_array)
        if solution_array_len != student_array_len:
            self.issues.append(
                message.format(
                    expected = solution_array_len,
                    actual=student_array_len,
                )
            )

class EqualityRule(Rule):
    def __call__(self, path, message):
        solution_field = safe_glom(self.solution_pivot_table, path)
        student_field = safe_glom(self.student_pivot_table, path)
        if solution_field != student_field:
            self.issues.append(
                message.format(expected=solution_field, actual=student_field)
            )


class ExistenceRule(Rule):
    def __call__(self, path, message):
        if not is_empty(safe_glom(self.solution_pivot_table, path)) and is_empty(
            safe_glom(self.student_pivot_table, path)
        ):
            self.issues.append(message)


class OverExistenceRule(Rule):
    def __call__(self, path, message):
        if is_empty(safe_glom(self.solution_pivot_table, path)) and not is_empty(
            safe_glom(self.student_pivot_table, path)
        ):
            self.issues.append(message)


rule_types = {
    "array_equal_length": ArrayEqualLengthRule,
    "array_equality": ArrayEqualityRule,
    "equality": EqualityRule,
    "existence": ExistenceRule,
    "over_existence": OverExistenceRule,
}


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
                )
            )
            bound_rules["array_equal_length"](
                "rows",
                (
                    "The number of rows is incorrect. "
                    "Expected {expected}, but got {actual}."
                )
            )
            bound_rules["array_equal_length"](
                "columns",
                (
                    "The number of columns is incorrect. "
                    "Expected {expected}, but got {actual}."
                )
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
