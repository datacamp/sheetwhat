from protowhat.Feedback import Feedback
from protowhat.State import State as BaseState
import copy

from protowhat.Test import Fail

from sheetwhat.selectors import Dispatcher


class State(BaseState):
    def __init__(
        self, student_data, solution_data, sct_range, reporter, force_diagnose=False
    ):
        self.student_data = student_data
        self.solution_data = solution_data
        self.sct_range = sct_range
        self.reporter = reporter
        self.messages = []
        self.creator = None
        self.dispatcher = Dispatcher()
        self.node_name = "root"
        self.force_diagnose = force_diagnose

    def report(self, feedback: str):
        return self.do_test(Fail(Feedback(feedback)))

    def to_child(self, append_message="", node_name=None, **kwargs):
        """Basic implementation of returning a child state"""
        child = copy.deepcopy(self)
        for kwarg in kwargs:
            setattr(child, kwarg, kwargs[kwarg])
        child.node_name = node_name
        if not isinstance(append_message, dict):
            append_message = {"msg": append_message, "kwargs": {}}
        child.messages = [*self.messages, append_message]
        return child

    def to_message_exposed_dict(self):
        """This dictionary is passed through to the message formatter. The fields
        defined in the dictionary can be replaced by values in the state by using
        the classical {field} notation."""
        return {"range": self.sct_range}
