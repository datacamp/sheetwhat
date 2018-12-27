from protowhat.Reporter import Reporter

from .utils import lower_first, upper_first


class FirstIssueFormatter:
    def __call__(self, root_message, issues):
        root_message = upper_first(root_message)
        first_issue_message = lower_first(issues[0])
        return f"{root_message}, {first_issue_message}."


formatters = {"first_issue": FirstIssueFormatter}


class SheetwhatReporter(Reporter):
    def __init__(self):
        super().__init__()

    def do_test(
        self,
        feedback_or_root_message,
        issues=None,
        formatting_strategy="first_issue",
        formatting_options={},
    ):
        if isinstance(issues, list) and len(issues) > 0:
            formatter = formatters[formatting_strategy](**formatting_options)
            return super().do_test(formatter(feedback_or_root_message, issues))
        else:
            return super().do_test(feedback_or_root_message)
