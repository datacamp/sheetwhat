from protowhat.State import State as BaseState


class State(BaseState):
    def __init__(self, student_data, solution_data, sct_range, reporter):
        self.student_data = student_data
        self.solution_data = solution_data
        self.sct_range = sct_range
        self.reporter = reporter

    def do_test(self, feedback_message, highlight=None):
        return self.reporter.do_test(feedback_message)
