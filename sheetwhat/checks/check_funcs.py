from .utils import crop_by_range
import copy


def has_code(
    state,
    text,
    incorrect_msg="The checker expected to find `{{text}}` in your command.",
    fixed=False,
):
    """TODO
    """

    return state

def round_array_2d(array_2d, ndigits):
    return [ [ round(x, ndigits) if isinstance(x, (int, float)) else x for x in row ] for row in array_2d ]

def is_empty_2d(x):
    return False
    # return all(map(is_empty, x) if isinstance(x, list) else x

def check_range(state, missing_msg=None):

    student_values = crop_by_range(state.student_data["values"], state.sct_range)
    solution_values = crop_by_range(state.solution_data["values"], state.sct_range)

    if is_empty_2d(student_values) and not is_empty_2d(solution_values):
       _msg = missing_msg or f"Please fill in `{state.sct_range}` to complete the exercise."
       state.do_test(_msg)

    return state.to_child({** copy.deepcopy(state.student_data), 'values': student_values},
                          {** copy.deepcopy(state.solution_data), 'values': solution_values})

def has_equal_value(state, incorrect_msg=None, ndigits=4):
    child = check_range(state)

    student_values_rounded = round_array_2d(child.student_data['values'], ndigits)
    solution_values_rounded = round_array_2d(child.solution_data['values'], ndigits)

    if student_values_rounded != solution_values_rounded:
        _msg = incorrect_msg or f"The value at `{state.sct_range}` is not correct."
        state.do_test(_msg)

    return state
