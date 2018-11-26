from .rules import rule_types


def has_equal_conditional_formats(state, absolute=False, incorrect_msg=None):
    student_cond_formats = state.student_data["conditionalFormats"]
    solution_cond_formats = state.solution_data["conditionalFormats"]

    issues = []
    bound_rules = {
        key: RuleClass(student_cond_formats, solution_cond_formats, issues)
        for key, RuleClass in rule_types.items()
    }

    bound_rules["array_equality"](
        ["ranges"], "There ranges of the {ordinal} rule are incorrect."
    ),
    bound_rules["array_equality"](
        ["booleanRule.condition"], "There condition of the {ordinal} rule is incorrect."
    ),
    bound_rules["array_equality"](
        ["gradientRule.condition"], "There condition of the {ordinal} is incorrect."
    ),
    bound_rules["array_equality"](
        ["booleanRule.format"], "There format of the {ordinal} rule is incorrect."
    ),
    bound_rules["array_equality"](
        ["gradientRule.format"], "There format of the {ordinal} rule is incorrect."
    ),

    nb_issues = len(issues)
    if nb_issues > 0:
        _issues_msg = "\n".join([f"- {issue}" for issue in issues])
        _msg = (
            f"There {'are' if nb_issues > 1 else 'is'} {nb_issues} "
            f"issue{'s' if nb_issues > 1 else ''} with the conditional "
            f"formatting rules:\n\n{_issues_msg}\n"
        )
        state.do_test(_msg)
