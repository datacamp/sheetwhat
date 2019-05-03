from .check_funcs import check_range
from sheetwhat.selectors import Dispatcher


def has_equal_data_validation(state, incorrect_msg=None):
    child = check_range(state, field="dataValidations", field_msg="data validation")

    student_data_validation = child.student_data
    solution_data_validation = child.solution_data

    message = "In cell `{range}`, did you use the correct data validation?"

    # For now, we generally only support cells, not ranges. This means we always
    # have to look at the content at index 0, 0.
    condition_path = "0.0.condition"
    student_data_validation_condtion = Dispatcher().select(
        condition_path, student_data_validation
    )
    solution_data_validation_condtion = Dispatcher().select(
        condition_path, solution_data_validation
    )
    if student_data_validation_condtion != solution_data_validation_condtion:
        child.report(
            (incorrect_msg or message).format(**state.to_message_exposed_dict())
        )

    return state
