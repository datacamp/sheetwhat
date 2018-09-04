from sheetwhat.checks import check_range
from .utils import is_empty
import glom
import functools
from protowhat import selectors


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
