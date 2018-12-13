from protowhat.State import State as BaseState
import copy


class State(BaseState):
    def __init__(self, student_data, solution_data, sct_range, reporter):
        self.student_data = student_data
        self.solution_data = solution_data
        self.sct_range = sct_range
        self.reporter = reporter
        self.node_name = "root"
        self.prepend_msg = ""

    def do_test(self, feedback_message, highlight=None):
        return self.reporter.do_test(feedback_message)

    def to_child(self, student_data, solution_data, prepend_msg="", node_name=None):
        """Basic implementation of returning a child state"""

        child = copy.deepcopy(self)
        child.student_data = student_data
        child.solution_data = solution_data
        child.prepend_msg = self.prepend_msg + prepend_msg
        child.node_name = node_name
        child.parent = self
        return child

    def to_message_exposed_dict(self):
        """This dictionary is passed through to the message formatter. The fields
        defined in the dictionary can be replaced by values in the state by using
        the classical {field} notation."""
        return {"range": self.sct_range}
