import copy
from functools import partial

from protowhat import selectors
from protowhat.Reporter import TestRunnerProxy

from sheetwhat.Test import ExistenceTest, EqualityTest
from sheetwhat.selectors import dispatcher_selector
from sheetwhat.utils import normalize_formula

from ..Range import Range


def conditional_format_filter(sct_range, conditional_format_data):
    for conditional_format_range in conditional_format_data.get("ranges", []):
        conditional_format_range_obj = Range(conditional_format_range)
        if Range(sct_range).is_within(conditional_format_range_obj):
            return True
    return False


def has_equal_conditional_formats(state, absolute=False, incorrect_msg=None):
    sct_range_filter = partial(conditional_format_filter, state.sct_range)
    student_cond_formats = list(
        filter(sct_range_filter, state.student_data["conditionalFormats"])
    )
    solution_cond_formats = list(
        filter(sct_range_filter, state.solution_data["conditionalFormats"])
    )

    test_runner = TestRunnerProxy(state.reporter)

    if len(student_cond_formats) < len(solution_cond_formats):
        state.report(
            f"There aren't enough conditional format rules defined at `{state.sct_range}`."
        )

    for i, (student_cond_format, solution_cond_format) in enumerate(
        zip(student_cond_formats, solution_cond_formats)
    ):
        ordinal = selectors.get_ord(i + 1)

        selector = dispatcher_selector(student_cond_format, solution_cond_format)

        test_runner.do_test(
            ExistenceTest(
                *selector("booleanRule"),
                f"The {ordinal} rule is incorrect, expected single color.",
            )
        )
        test_runner.do_test(
            ExistenceTest(
                *selector("gradientRule"),
                f"The {ordinal} rule is incorrect, expected color scale.",
            )
        )
        if not test_runner.has_failed:

            def normalize_condition(condition):
                if condition and condition.get("type", None) == "CUSTOM_FORMULA":
                    condition = copy.deepcopy(condition)
                    condition["values"][0]["userEnteredValue"] = normalize_formula(
                        condition["values"][0]["userEnteredValue"]
                    )
                return condition

            tests = [
                EqualityTest(
                    *map(normalize_condition, selector("booleanRule.condition")),
                    f"The condition of the {ordinal} rule is incorrect.",
                ),
                EqualityTest(
                    *selector("booleanRule.format"),
                    f"The format of the {ordinal} rule is incorrect.",
                ),
                EqualityTest(
                    *selector("gradientRule.minpoint"),
                    f"The minpoint of the {ordinal} rule is incorrect.",
                ),
                EqualityTest(
                    *selector("gradientRule.midpoint"),
                    f"The minpoint of the {ordinal} rule is incorrect.",
                ),
                EqualityTest(
                    *selector("gradientRule.maxpoint"),
                    f"The maxpoint of the {ordinal} rule is incorrect.",
                ),
            ]

            test_runner.do_tests(tests)

    nb_issues = len(test_runner.failures)
    if nb_issues > 0:
        _issues_msg = "\n".join(
            [f"- {test.feedback.message}" for test in test_runner.failures]
        )
        _msg = (
            f"There {'are' if nb_issues > 1 else 'is'} {nb_issues} "
            f"issue{'s' if nb_issues > 1 else ''} with the conditional "
            f"formatting rules:\n\n{_issues_msg}\n"
        )
        state.report(_msg)
