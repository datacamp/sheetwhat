import requests
import pytest
import json


from sheetwhat.State import State
from protowhat.Reporter import Reporter
from protowhat.Test import TestFail as TF

from functools import reduce
from copy import deepcopy
from contextlib import contextmanager

def setup_state(stu, sol, sct_range):
    return State(stu, sol, sct_range, reporter=Reporter())

@contextmanager
def verify_success(should_pass):
    if should_pass:
        yield
    else:
        with pytest.raises(TF):
            yield



def try_exercise(solution_data, user_data, sct):
    from sheetwhat.test_exercise import test_exercise

    result = test_exercise(sct, user_data, solution_data)

    return {"success": result.get("correct", False), "message": result.get("message")}


class Identity:
    def __repr__(self):
        return "Identity()"

    def __call__(self, x):
        return x


class Mutation:
    def __init__(self, path, value):
        self.path = path
        self.value = value

    def __repr__(self):
        return f"Mutation({json.dumps(self.path)}, {json.dumps(self.value)})"

    def __call__(self, obj):
        copy = deepcopy(obj)
        nested_obj = copy
        i = 0
        while i < len(self.path) - 1:
            field = self.path[i]
            nested_obj = nested_obj[field]
            i += 1
        nested_obj[self.path[i]] = self.value
        return copy


class Addition:
    def __init__(self, path, value):
        self.path = path
        self.value = value

    def __repr__(self):
        return f"Addition({json.dumps(self.path)}, {json.dumps(self.value)})"

    def __call__(self, obj):
        copy = deepcopy(obj)
        nested_obj = copy
        i = 0
        while i < len(self.path) - 1:
            field = self.path[i]
            nested_obj = nested_obj[field]
            i += 1
        nested_obj[self.path[i]].append(self.value)
        return copy


class Deletion:
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Deletion({json.dumps(self.path)})"

    def __call__(self, obj):
        copy = deepcopy(obj)
        nested_obj = copy
        i = 0
        while i < len(self.path) - 1:
            field = self.path[i]
            nested_obj = nested_obj[field]
            i += 1
        del nested_obj[self.path[i]]
        return copy


def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
