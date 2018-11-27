from .rules import rule_types
from protowhat import selectors


def has_equal_conditional_formats(state, absolute=False, incorrect_msg=None):
    student_cond_formats = state.student_data["conditionalFormats"]
    solution_cond_formats = state.solution_data["conditionalFormats"]

    issues = []

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
                "ranges", f"There ranges of the {ordinal} rule are incorrect."
            )

            bound_rules["equality"](
                "booleanRule.condition",
                f"There condition of the {ordinal} rule is incorrect.",
            )
            bound_rules["equality"](
                "booleanRule.format",
                f"There format of the {ordinal} rule is incorrect.",
            )

            bound_rules["equality"](
                "gradientRule.minpoint",
                f"There minpoint of the {ordinal} rule is incorrect.",
            )
            bound_rules["equality"](
                "gradientRule.midpoint",
                f"There minpoint of the {ordinal} rule is incorrect.",
            )
            bound_rules["equality"](
                "gradientRule.maxpoint",
                f"There maxpoint of the {ordinal} rule is incorrect.",
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
