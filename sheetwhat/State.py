from protowhat.State import State as BaseState
import copy


class State(BaseState):
    def __init__(self, student_data, solution_data, sct_range, reporter):
        self.student_data = student_data
        self.solution_data = solution_data
        self.sct_range = sct_range
        self.reporter = reporter
        self.node_name = "root"
        self.root_message = ""

    def set_root_message(self, message):
        assert isinstance(message, str)
        self.root_message = message

    def do_test(self, message_or_issues, *args, **kwargs):
        is_list = isinstance(message_or_issues, list)
        is_str = isinstance(message_or_issues, str)
        assert is_list or is_str
        if is_list:
            return self.reporter.do_test(
                self.root_message, message_or_issues, *args, **kwargs
            )
        if is_str:
            return self.reporter.do_test(message_or_issues)

    def to_child(self, student_data, solution_data, node_name=None):
        """Basic implementation of returning a child state"""
        child = copy.deepcopy(self)
        child.student_data = student_data
        child.solution_data = solution_data
        child.node_name = node_name
        child.parent = self
        return child

    def to_message_exposed_dict(self):
        """This dictionary is passed through to the message formatter. The fields
        defined in the dictionary can be replaced by values in the state by using
        the classical {field} notation."""
        return {"range": self.sct_range}
