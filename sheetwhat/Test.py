import copy
import functools

from abc import ABC

from protowhat import selectors
from protowhat.Test import Test
from protowhat.Feedback import Feedback as ProtoFeedback

from sheetwhat.utils import is_empty, dict_keys, normalize_formula


class Feedback(ProtoFeedback):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SolutionBasedTest(Test, ABC):
    def __init__(self, student_data, solution_data, feedback):
        super().__init__(feedback)
        self.student_data = student_data
        self.solution_data = solution_data


def array_element_tests(test, student_data, solution_data, feedback, *args, **kwargs):
    tests = []
    if not isinstance(student_data, list) or not isinstance(solution_data, list):
        # todo: no feedback? what is the use case?
        return tests
    for i, element_data in enumerate(zip(student_data, solution_data)):
        if isinstance(feedback, str):
            item_feedback = Feedback(feedback)
        else:
            item_feedback = copy.deepcopy(feedback)
        item_feedback.message = item_feedback.message.format(
            ordinal=selectors.get_ord(i + 1),
            expected=solution_data[i],
            actual=student_data[i],
        )
        tests.append(test(*element_data, item_feedback, *args, **kwargs))
    return tests


class ArrayEqualityTest(SolutionBasedTest):
    # todo: not used anymore
    # todo: for a Test like this to work, one of these is needed:
    #  - recursive test() call returning and running subtests
    #  - test.feedback is a list
    #  - test.feedback can be both a list or a single feedback instance
    def __init__(self, *args, equal_func=lambda x, y: x == y):
        super().__init__(*args)
        self.equal_func = equal_func

    def test(self):
        if not isinstance(self.student_data, list) or not isinstance(
            self.solution_data, list
        ):
            return
        if self.student_data != self.solution_data:
            self.result = False

            # TODO
            matches = [
                self.equal_func(x, y)
                for x, y in zip(self.student_data, self.solution_data)
            ]

            def mismatch_reducer(all, x):
                return all if x[1] else [*all, x[0]]

            mismatch_indices = functools.reduce(
                mismatch_reducer, enumerate(matches), []
            )

            self.feedback.issues.extend(
                [
                    self.feedback.message.format(
                        ordinal=selectors.get_ord(i + 1),
                        expected=self.solution_data[i],
                        actual=self.student_data[i],
                    )
                    for i in mismatch_indices
                ]
            )
        else:
            self.result = True


class ArrayEqualLengthTest(SolutionBasedTest):
    def test(self):
        if not isinstance(self.student_data, list):
            return
        if not isinstance(self.solution_data, list) or len(self.solution_data) == 0:
            return  # TODO ?
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
            return
        solution_key_set = set(self.solution_data.keys())
        student_key_set = set(self.student_data.keys())
        if solution_key_set != student_key_set:
            self.result = False
            self.feedback.message = self.feedback.message.format(
                solution_keys=solution_key_set, student_keys=student_key_set
            )


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


class OverExistenceTest(SolutionBasedTest):
    def test(self):
        if is_empty(self.solution_data) and not is_empty(self.student_data):
            self.result = False


class SetEqualityTest(SolutionBasedTest):
    def test(self):
        if not isinstance(self.student_data, list) or not isinstance(
            self.solution_data, list
        ):
            return
        solution_set = set(self.solution_data)
        student_set = set(self.student_data)
        if solution_set != student_set:
            self.result = False
