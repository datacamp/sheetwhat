from protowhat.Feedback import FeedbackComponent
from protowhat.State import State as BaseState
import copy

from sheetwhat.selectors import Dispatcher


class State(BaseState):
    def __init__(
        self, student_data, solution_data, sct_range, reporter, force_diagnose=False
    ):
        self.student_data = student_data
        self.solution_data = solution_data
        self.sct_range = sct_range
        self.reporter = reporter
        self.feedback_context = None
        self.creator = None
        self.dispatcher = Dispatcher()
        self.node_name = "root"
        self.force_diagnose = force_diagnose
        self.debug = False

    def to_child(self, append_message="", node_name=None, **kwargs):
        """Basic implementation of returning a child state"""
        child = copy.deepcopy(self)
        for kwarg in kwargs:
            setattr(child, kwarg, kwargs[kwarg])
        child.node_name = node_name
        if not isinstance(append_message, FeedbackComponent):
            append_message = FeedbackComponent(append_message)
        child.feedback_context = append_message
        return child

    def get_feedback(self, conclusion):
        return self.feedback_cls(
            conclusion,
            [state.feedback_context for state in self.state_history],
        )

    def to_message_exposed_dict(self):
        """This dictionary is passed through to the message formatter. The fields
        defined in the dictionary can be replaced by values in the state by using
        the classical {field} notation."""
        return {"range": self.sct_range}
