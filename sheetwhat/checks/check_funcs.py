from sheetwhat.utils import (
    crop_by_range,
    is_empty,
    round_array_2d,
    normalize_array_2d,
    map_2d,
    normalize_formula,
)
import re


def check_range(state, field, field_msg, missing_msg=None):
    student_field_content = crop_by_range(state.student_data[field], state.sct_range)
    solution_field_content = crop_by_range(state.solution_data[field], state.sct_range)

    if is_empty(student_field_content):
        _msg = (missing_msg or "Please fill in a {field_msg} in `{range}`.").format(
            field_msg=field_msg, **state.to_message_exposed_dict()
        )
        state.report(_msg)

    return state.to_child(
        student_data=student_field_content, solution_data=solution_field_content
    )


def has_code(state, pattern, fixed=False, incorrect_msg=None, normalize=lambda x: x):
    child = check_range(state, field="formulas", field_msg="formula")

    def match(on_text):
        if fixed:
            return normalize(pattern) in str(on_text)
        else:
            return re.search(pattern, str(on_text)) is not None

    student_formulas_normalized = map_2d(normalize, child.student_data)
    student_matches = map_2d(match, student_formulas_normalized)

    if not all([all(row) for row in student_matches]):
        _msg = (
            incorrect_msg or "In cell `{range}`, did you use the correct formula?"
        ).format(**state.to_message_exposed_dict())
        child.report(_msg)

    return state


def check_function(state, name, missing_msg=None):
    missing_msg = (
        missing_msg or "In cell `{range}`, did you use the `{name}()` function?"
    ).format(name=name, **state.to_message_exposed_dict())

    has_code(
        state,
        pattern=name,
        fixed=True,
        incorrect_msg=missing_msg,
        normalize=normalize_formula,
    )
    # Don't return state; chaining not implemented yet
    return None


def check_operator(state, operator, missing_msg=None):
    missing_msg = (
        missing_msg or "In cell `{range}`, did you use the `{operator}` operator?"
    ).format(operator=operator, **state.to_message_exposed_dict())
    has_code(
        state,
        pattern=operator,
        fixed=True,
        incorrect_msg=missing_msg,
        normalize=normalize_formula,
    )
    # Don't return state; chaining not implemented yet
    return None


def has_equal_value(state, incorrect_msg=None, ndigits=4):
    child = check_range(state, field="values", field_msg="value")

    student_values_rounded = round_array_2d(child.student_data, ndigits)
    solution_values_rounded = round_array_2d(child.solution_data, ndigits)

    if student_values_rounded != solution_values_rounded:
        _msg = (incorrect_msg or "The value at `{range}` is not correct.").format(
            **child.to_message_exposed_dict()
        )

        child.report(_msg)

    return state


def has_equal_formula(state, incorrect_msg=None, ndigits=4):
    child = check_range(state, field="formulas", field_msg="formula")

    student_formulas_normalized = normalize_array_2d(child.student_data)
    solution_formulas_normalized = normalize_array_2d(child.solution_data)

    if student_formulas_normalized != solution_formulas_normalized:
        _msg = (
            incorrect_msg or "In cell `{range}`, did you use the correct formula?"
        ).format(**state.to_message_exposed_dict())
        child.report(_msg)

    return state


def has_equal_references(state, absolute=False, incorrect_msg=None):
    child = check_range(state, field="formulas", field_msg="formula")

    if absolute:
        pattern = r"\$?[A-Z]+\$?\d+(?:\:\$?[A-Z]+\$?\d+)?"
    else:
        pattern = r"[A-Za-z]+\d+(?:\:[A-Za-z]+\d+)?"

    student_formulas = child.student_data
    solution_formulas = child.solution_data

    for i, student_row in enumerate(student_formulas):
        for j, student_cell in enumerate(student_row):
            solution_cell = str(solution_formulas[i][j])
            student_cell = str(student_cell)
            solution_references = re.findall(pattern, solution_cell)

            for reference in solution_references:
                if normalize_formula(reference) not in normalize_formula(student_cell):
                    _msg = (
                        incorrect_msg
                        or (
                            "In cell `{range}`, did you use the{absolute_str} "
                            "reference `{reference}`?"
                        )
                    ).format(
                        absolute_str=" absolute" if absolute else "",
                        reference=reference,
                        **child.to_message_exposed_dict()
                    )
                    child.report(_msg)
