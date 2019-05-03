from protowhat.Reporter import TestRunnerProxy

from sheetwhat.checks import check_range
from sheetwhat.selectors import dispatcher_selector
from sheetwhat.utils import dict_keys, normalize_formula

from sheetwhat.Test import (
    ExistenceTest,
    OverExistenceTest,
    EqualityTest,
    SetEqualityTest,
    DictKeyEqualityTest,
    ArrayEqualLengthTest,
    array_element_tests,
)


def has_equal_pivot(state, extra_msg=None):
    child = check_range(state, field="pivotTables", field_msg="pivot table")

    student_pivot_tables = child.student_data
    solution_pivot_tables = child.solution_data

    for i, student_row in enumerate(student_pivot_tables):
        for j, student_pivot_table in enumerate(student_row):
            solution_pivot_table = solution_pivot_tables[i][j]

            test_runner = TestRunnerProxy(state.reporter)
            selector = dispatcher_selector(student_pivot_table, solution_pivot_table)

            tests = [
                ExistenceTest(*selector("rows"), "There are no rows."),
                ExistenceTest(*selector("columns"), "There are no columns."),
                ExistenceTest(*selector("values"), "There are no values."),
                ExistenceTest(*selector("criteria"), "There are no filters."),
                OverExistenceTest(
                    *selector("rows"), "There are rows but there shouldn't be."
                ),
                OverExistenceTest(
                    *selector("columns"), "There are columns but there shouldn't be."
                ),
                OverExistenceTest(
                    *selector("values"), "There are values but there shouldn't be."
                ),
                EqualityTest(*selector("source"), "The source data is incorrect."),
            ]

            tests += array_element_tests(
                EqualityTest,
                *selector(("rows", ["sortOrder"])),
                (
                    "Inside rows, expected the {ordinal} sort order to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("columns", ["sortOrder"])),
                (
                    "Inside columns, expected the {ordinal} sort order to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("rows", ["valueBucket"])),
                (
                    "Inside rows, expected the {ordinal} sort group to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("columns", ["valueBucket"])),
                (
                    "Inside columns, expected the {ordinal} sort group to be "
                    "`{expected}`, but got `{actual}`"
                ),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("rows", ["sourceColumnOffset"])),
                ("Inside rows, the {ordinal} grouping variable is incorrect."),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("columns", ["sourceColumnOffset"])),
                ("Inside columns, the {ordinal} grouping variable is incorrect."),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("rows", ["showTotals"])),
                ("Inside rows, the {ordinal} totals are not showing."),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("columns", ["showTotals"])),
                ("Inside columns, the {ordinal} totals are not showing."),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("values", ["summarizeFunction"])),
                (
                    "Inside values, expected the {ordinal} summarize function "
                    "to be `{expected}`, but got `{actual}`."
                ),
            )
            tests += array_element_tests(
                EqualityTest,
                *selector(("values", ["calculatedDisplayType"])),
                (
                    "Inside values, expected the {ordinal} display type "
                    "to be `{expected}`, but got `{actual}`."
                ),
            )

            tests += [
                ArrayEqualLengthTest(
                    *selector("values"),
                    (
                        "The number of values is incorrect. "
                        "Expected {expected}, but got {actual}."
                    ),
                ),
                ArrayEqualLengthTest(
                    *selector("rows"),
                    (
                        "The number of rows is incorrect. "
                        "Expected {expected}, but got {actual}."
                    ),
                ),
                ArrayEqualLengthTest(
                    *selector("columns"),
                    (
                        "The number of columns is incorrect. "
                        "Expected {expected}, but got {actual}."
                    ),
                ),
            ]

            tests.append(
                DictKeyEqualityTest(
                    *selector("criteria"),
                    "The rows or columns used in the filter are incorrect.",
                )
            )
            for key in dict_keys(*selector("criteria")):
                tests.append(
                    SetEqualityTest(
                        *selector(f"criteria.{key}.visibleValues"),
                        "The filtered out values are incorrect.",
                    )
                )

            tests += array_element_tests(
                EqualityTest,
                *selector(("values", ["formula"])),
                "The {ordinal} value does not contain the correct calculated field.",
                lambda x, y: normalize_formula(x) == normalize_formula(y),
            )

            test_runner.do_tests(tests)

            nb_issues = len(test_runner.failures)
            if nb_issues > 0:
                _issues_msg = "\n".join(
                    [f"- {test.feedback.message}" for test in test_runner.failures]
                )
                _msg = (
                    f"There {'are' if nb_issues > 1 else 'is'} {nb_issues} "
                    f"issue{'s' if nb_issues > 1 else ''} with the pivot table "
                    f"at `{child.sct_range}`:\n\n{_issues_msg}\n"
                )
                child.report(_msg)
