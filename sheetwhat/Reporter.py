from .utils import lower_first, upper_first


class FirstIssueFormatter:
    def __call__(self, root_message, issues):
        root_message = upper_first(root_message)
        first_issue_message = lower_first(issues[0])
        return f"{root_message}, {first_issue_message}."


formatters = {"first_issue": FirstIssueFormatter}
