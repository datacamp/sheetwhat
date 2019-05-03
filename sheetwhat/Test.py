import copy

from abc import ABC

from protowhat import selectors
from protowhat.Test import Test
from protowhat.Feedback import Feedback

from sheetwhat.utils import is_empty


class SolutionBasedTest(Test, ABC):
    def __init__(self, student_data, solution_data, feedback):
        super().__init__(feedback)
        self.student_data = student_data
        self.solution_data = solution_data

    def __repr__(self):
        return f"{self.__class__.__name__}:" \
            f"student data = {self.student_data}" \
            f"solution data = {self.solution_data}"


def array_element_tests(test, student_data, solution_data, feedback, *args, **kwargs):
    tests = []
    if not isinstance(student_data, list) or not isinstance(solution_data, list):
        # If student data is None; Feedback will be provided by a different test.
        return tests
    for i, (element_student_data, element_solution_data) in enumerate(
        zip(student_data, solution_data)
    ):
        if isinstance(feedback, str):
            item_feedback = Feedback(feedback)
        else:
            item_feedback = copy.deepcopy(feedback)
        item_feedback.message = item_feedback.message.format(
            ordinal=selectors.get_ord(i + 1),
            expected=element_solution_data,
            actual=element_student_data,
        )
        tests.append(
            test(
                element_student_data,
                element_solution_data,
                item_feedback,
                *args,
                **kwargs,
            )
        )
    return tests


class ArrayEqualLengthTest(SolutionBasedTest):
    def test(self):
        if (
            not isinstance(self.student_data, list)
            or not isinstance(self.solution_data, list)
            or len(self.solution_data) == 0
        ):
            self.result = True
        else:
            solution_array_len = len(self.solution_data)
            student_array_len = len(self.student_data)
            if solution_array_len != student_array_len:
                self.result = False
                self.feedback.message = self.feedback.message.format(
                    expected=solution_array_len, actual=student_array_len
                )
            else:
                self.result = True


class DictKeyEqualityTest(SolutionBasedTest):
    def test(self):
        if not isinstance(self.student_data, dict) or not isinstance(
            self.solution_data, dict
        ):
            self.result = True
        else:
            solution_key_set = set(self.solution_data.keys())
            student_key_set = set(self.student_data.keys())
            if solution_key_set != student_key_set:
                self.result = False
                self.feedback.message = self.feedback.message.format(
                    solution_keys=solution_key_set, student_keys=student_key_set
                )
            else:
                self.result = True


class EqualityTest(SolutionBasedTest):
    def __init__(
        self, student_data, solution_data, feedback, equal_func=lambda x, y: x == y
    ):
        super().__init__(student_data, solution_data, feedback)
        self.equal_func = equal_func

    def test(self):
        if self.equal_func(self.student_data, self.solution_data):
            self.result = True
        else:
            self.result = False
            self.feedback.message = self.feedback.message.format(
                expected=self.solution_data, actual=self.student_data
            )


class ExistenceTest(SolutionBasedTest):
    def test(self):
        if not is_empty(self.solution_data) and is_empty(self.student_data):
            self.result = False
        else:
            self.result = True


class OverExistenceTest(SolutionBasedTest):
    def test(self):
        if is_empty(self.solution_data) and not is_empty(self.student_data):
            self.result = False
        else:
            self.result = True


class SetEqualityTest(SolutionBasedTest):
    def test(self):
        if not isinstance(self.student_data, list) or not isinstance(
            self.solution_data, list
        ):
            self.result = True
        else:
            solution_set = set(self.solution_data)
            student_set = set(self.student_data)
            if solution_set != student_set:
                self.result = False
            else:
                self.result = True
