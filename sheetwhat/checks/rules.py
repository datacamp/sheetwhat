import glom
import functools
from sheetwhat.utils import is_empty, dict_keys, normalize_formula
from protowhat import selectors

from ..utils import lower_first

# Supercharge path with appropriate coalesce at every level
# E.g.
#  deep_coalesce("path", None) => Coalesce("path", default=None)
#  deep_coalesce(("path", ), None) =>
#    Coalesce((Coalesce("path", default=None),), default=None)
# etc. (tuples and lists work analogously)
def deep_coalesce(path, default):
    if isinstance(path, (tuple, list)):
        path = type(path)(deep_coalesce(p, default) for p in path)
    return glom.Coalesce(path, default=default)


def safe_glom(obj, path, fallback=None):
    return glom.glom(obj, deep_coalesce(path, fallback))


class Rule:
    def __init__(self, student_structure, solution_structure, issues):
        self.student_structure = student_structure
        self.solution_structure = solution_structure
        self.issues = issues

    def __call__(self, *args, tag=None, **kwargs):
        self.call(*args, **kwargs)


class ArrayEqualityRule(Rule):
    def call(self, path, message, equal_func=lambda x, y: x == y):
        solution_array = safe_glom(self.solution_structure, path)
        student_array = safe_glom(self.student_structure, path)
        if not isinstance(student_array, list):
            return
        if not isinstance(solution_array, list):
            return
        if solution_array != student_array:
            matches = [equal_func(x, y) for x, y in zip(student_array, solution_array)]
            mismatch_reducer = lambda all, x: all if x[1] else [*all, x[0]]
            mismatch_indices = functools.reduce(
                mismatch_reducer, enumerate(matches), []
            )

            self.issues.extend(
                [
                    message.format(
                        ordinal=selectors.get_ord(i + 1),
                        expected=solution_array[i],
                        actual=student_array[i],
                    )
                    for i in mismatch_indices
                ]
            )


class ArrayEqualLengthRule(Rule):
    def call(self, path, message):
        solution_array = safe_glom(self.solution_structure, path)
        student_array = safe_glom(self.student_structure, path)
        if not isinstance(student_array, list):
            return
        if not isinstance(solution_array, list) or len(solution_array) == 0:
            return
        solution_array_len = len(solution_array)
        student_array_len = len(student_array)
        if solution_array_len != student_array_len:
            self.issues.append(
                message.format(expected=solution_array_len, actual=student_array_len)
            )


class DictKeyEqualityRule(Rule):
    def call(self, path, message):
        solution_dict = safe_glom(self.solution_structure, path)
        student_dict = safe_glom(self.student_structure, path)
        if not isinstance(student_dict, dict) or not isinstance(solution_dict, dict):
            return
        solution_key_set = set(solution_dict.keys())
        student_key_set = set(student_dict.keys())
        if solution_key_set != student_key_set:
            self.issues.append(
                message.format(
                    solution_keys=solution_key_set, student_keys=student_key_set
                )
            )


class EqualityRule(Rule):
    def call(self, path, message, equal_func=lambda x, y: x == y):
        solution_field = safe_glom(self.solution_structure, path)
        student_field = safe_glom(self.student_structure, path)
        if not equal_func(student_field, solution_field):
            self.issues.append(
                message.format(expected=solution_field, actual=student_field)
            )


class ExistenceRule(Rule):
    def call(self, path, message):
        if not is_empty(safe_glom(self.solution_structure, path)) and is_empty(
            safe_glom(self.student_structure, path)
        ):
            self.issues.append(message)


class OverExistenceRule(Rule):
    def call(self, path, message):
        if is_empty(safe_glom(self.solution_structure, path)) and not is_empty(
            safe_glom(self.student_structure, path)
        ):
            self.issues.append(message)


class SetEqualityRule(Rule):
    def call(self, path, message):
        solution_array = safe_glom(self.solution_structure, path)
        student_array = safe_glom(self.student_structure, path)
        if not isinstance(student_array, list) or not isinstance(solution_array, list):
            return
        solution_set = set(solution_array)
        student_set = set(student_array)
        if solution_set != student_set:
            self.issues.append(message)


rule_types = {
    "array_equal_length": ArrayEqualLengthRule,
    "array_equality": ArrayEqualityRule,
    "dict_key_equality": DictKeyEqualityRule,
    "equality": EqualityRule,
    "existence": ExistenceRule,
    "over_existence": OverExistenceRule,
    "set_equality": SetEqualityRule,
}


def with_rules(func):
    @functools.wraps(func)
    def wrapper_with_rules(state, *args, **kwargs):
        issues = []
        bound_rules = {
            key: RuleClass(state.student_data, state.solution_data, issues)
            for key, RuleClass in rule_types.items()
        }
        result = func(state, *args, rules=bound_rules, **kwargs)
        nb_issues = len(issues)
        if nb_issues > 0:
            state.do_test(issues)
        return result

    return wrapper_with_rules
