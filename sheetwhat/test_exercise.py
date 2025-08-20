from protowhat.failure import Failure, InstructorError
from protowhat.Reporter import Reporter
from protowhat.sct_context import get_checks_dict, create_sct_context

from sheetwhat import checks
from sheetwhat.State import State


def test_exercise(
    sct, student_data, solution_data, success_msg=None, force_diagnose=False
):
    """
    """

    assert isinstance(sct, list)
    assert isinstance(student_data, dict)
    assert isinstance(solution_data, dict)

    reporter = Reporter()

    # the available SCT methods
    sct_dict = get_checks_dict(checks)

    # the available global variables
    sct_context = create_sct_context(sct_dict)
    Ex = sct_context["Ex"]

    for single_sct in sct:
        try:
            state = State(
                student_data=student_data,
                solution_data=solution_data,
                sct_range=single_sct.get("range"),
                reporter=reporter,
                force_diagnose=force_diagnose,
            )

            # setting manually to not run create_sct_context in loop
            Ex.root_state = state

            exec("\n".join(single_sct.get("sct", [])), sct_context)

        except Failure as e:
            if isinstance(e, InstructorError):
                # TODO: decide based on context
                raise e
            return reporter.build_failed_payload(e.feedback)

    if success_msg and isinstance(success_msg, str):
        reporter.success_msg = success_msg

    return reporter.build_final_payload()
