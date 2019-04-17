from sheetwhat.selectors import Dispatcher
from sheetwhat.checks.check_funcs import check_range

number_format_types = {
    "TEXT": "text",
    "NUMBER": "a number",
    "PERCENT": "a percent",
    "CURRENCY": "a currency",
    "DATE": "a date",
    "TIME": "a time",
    "DATE_TIME": "a date time",
    "SCIENTIFIC": "a scientific number",
}


def has_equal_number_format(state, incorrect_msg=None):
    child = check_range(state, field="numberFormats", field_msg="number format")

    student_number_format = child.student_data
    solution_number_format = child.solution_data

    generated_message = None
    standard_message = "In cell `{range}`, did you use the correct number format?"

    # For now, we generally only support cells, not ranges. This means we always
    # have to look at the content at index 0, 0.
    type_path = "0.0.numberFormat.type"
    student_number_format_type = Dispatcher().select(type_path, student_number_format)
    solution_number_format_type = Dispatcher().select(type_path, solution_number_format)
    if student_number_format_type != solution_number_format_type:
        actual_type = number_format_types.get(student_number_format_type)
        expected_type = number_format_types.get(solution_number_format_type)
        if actual_type is None or expected_type is None:
            generated_message = standard_message
        else:
            generated_message = (
                standard_message + f" Expected {expected_type}, but got {actual_type}."
            )
    elif student_number_format != solution_number_format:
        generated_message = standard_message

    if generated_message is not None:
        child.report(
            (incorrect_msg or generated_message).format(
                **state.to_message_exposed_dict()
            )
        )

    return state
