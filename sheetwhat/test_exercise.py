from protowhat.failure import Failure, InstructorError
from protowhat.Reporter import Reporter

from sheetwhat.sct_syntax import SCT_CTX
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
    for single_sct in sct:
        state = State(
            student_data=student_data,
            solution_data=solution_data,
            sct_range=single_sct.get("range"),
            reporter=reporter,
            force_diagnose=force_diagnose
        )

        SCT_CTX["Ex"].root_state = state

        try:
            exec("\n".join(single_sct.get("sct", [])), SCT_CTX)
        except Failure as e:
            if isinstance(e, InstructorError):
                # TODO: decide based on context
                raise e
            return reporter.build_failed_payload(e.feedback)

    if success_msg and isinstance(success_msg, str):
        reporter.success_msg = success_msg

    return reporter.build_final_payload()
