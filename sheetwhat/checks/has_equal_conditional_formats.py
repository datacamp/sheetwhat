from protowhat import selectors
import functools

from .rules import rule_types
from ..Range import Range


class ConditionalFormatFilter:
    def __init__(self, sct_range):
        self.sct_range = Range(sct_range)

    def __call__(self, conditional_format):
        for conditional_format_range in conditional_format.get("ranges", []):
            conditional_format_range_obj = Range(conditional_format_range)
            if self.sct_range.is_within(conditional_format_range_obj):
                return True
        return False


def has_equal_conditional_formats(state, absolute=False, incorrect_msg=None):
    sct_range_filter = ConditionalFormatFilter(state.sct_range)
    student_cond_formats = list(
        filter(sct_range_filter, state.student_data["conditionalFormats"])
    )
    solution_cond_formats = list(
        filter(sct_range_filter, state.solution_data["conditionalFormats"])
    )

    issues = []

    if len(student_cond_formats) < len(solution_cond_formats):
        state.do_test(
            f"There aren't enough conditional format rules defined at `{state.sct_range}`."
        )

    for i, (student_cond_format, solution_cond_format) in enumerate(
        zip(student_cond_formats, solution_cond_formats)
    ):
        ordinal = selectors.get_ord(i + 1)
        bound_rules = {
            key: RuleClass(student_cond_format, solution_cond_format, issues)
            for key, RuleClass in rule_types.items()
        }

        bound_rules["existence"](
            "booleanRule", f"The {ordinal} rule is incorrect, expected single color."
        )
        bound_rules["existence"](
            "gradientRule", f"The {ordinal} rule is incorrect, expected color scale."
        )
        if len(issues) == 0:
            bound_rules["equality"](
                "booleanRule.condition",
                f"The condition of the {ordinal} rule is incorrect.",
            )
            bound_rules["equality"](
                "booleanRule.format",
                f"The format of the {ordinal} rule is incorrect.",
            )

            bound_rules["equality"](
                "gradientRule.minpoint",
                f"The minpoint of the {ordinal} rule is incorrect.",
            )
            bound_rules["equality"](
                "gradientRule.midpoint",
                f"The minpoint of the {ordinal} rule is incorrect.",
            )
            bound_rules["equality"](
                "gradientRule.maxpoint",
                f"The maxpoint of the {ordinal} rule is incorrect.",
            )

    nb_issues = len(issues)
    if nb_issues > 0:
        _issues_msg = "\n".join([f"- {issue}" for issue in issues])
        _msg = (
            f"There {'are' if nb_issues > 1 else 'is'} {nb_issues} "
            f"issue{'s' if nb_issues > 1 else ''} with the conditional "
            f"formatting rules:\n\n{_issues_msg}\n"
        )
        state.do_test(_msg)
