from .utils import (
    crop_by_range,
    is_empty,
    round_array_2d,
    normalize_array_2d,
    map_2d,
    normalize_formula,
)
import copy
import re


def has_code(state, pattern, fixed=False, incorrect_msg=None, normalize=lambda x: x):
    child = check_range(state, field="formulas", field_msg="formula")

    def match(on_text):
        if fixed:
            return normalize(pattern) in str(on_text)
        else:
            return re.search(pattern, str(on_text)) is not None

    student_formulas_normalized = map_2d(normalize, child.student_data["formulas"])
    student_matches = map_2d(match, student_formulas_normalized)

    if sum([sum(row) for row in student_matches]) == 0:
        _msg = incorrect_msg or f"The formula at `{child.sct_range}` is not correct."
        child.do_test(_msg)

    return state


def check_function(state, name, missing_msg=None):
    has_code(state, pattern=name, fixed=True, normalize=normalize_formula)
    # Don't return state; chaining not implemented yet
    return None


def check_operator(state, operator, missing_msg=None):
    has_code(state, pattern=operator, fixed=True, normalize=normalize_formula)
    # Don't return state; chaining not implemented yet
    return None


def check_range(state, field, field_msg, missing_msg=None):

    student_field_content = crop_by_range(state.student_data[field], state.sct_range)
    solution_field_content = crop_by_range(state.solution_data[field], state.sct_range)

    if is_empty(student_field_content) and not is_empty(solution_field_content):
        _msg = (
            missing_msg
            or f"Please fill in a {field_msg} in `{state.sct_range}` to complete the exercise."
        )
        state.do_test(_msg)

    return state.to_child(
        {**copy.deepcopy(state.student_data), field: student_field_content},
        {**copy.deepcopy(state.solution_data), field: solution_field_content},
    )


def has_equal_value(state, incorrect_msg=None, ndigits=4):
    child = check_range(state, field="values", field_msg="value")

    student_values_rounded = round_array_2d(child.student_data["values"], ndigits)
    solution_values_rounded = round_array_2d(child.solution_data["values"], ndigits)

    if student_values_rounded != solution_values_rounded:
        _msg = incorrect_msg or f"The value at `{child.sct_range}` is not correct."
        child.do_test(_msg)

    return state


def has_equal_formula(state, incorrect_msg=None, ndigits=4):
    child = check_range(state, field="formulas", field_msg="formula")

    student_formulas_normalized = normalize_array_2d(child.student_data["formulas"])
    solution_formulas_normalized = normalize_array_2d(child.solution_data["formulas"])

    if student_formulas_normalized != solution_formulas_normalized:
        _msg = incorrect_msg or f"The formula at `{child.sct_range}` is not correct."
        child.do_test(_msg)

    return state
