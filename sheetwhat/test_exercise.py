from protowhat.Test import TestFail
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

    rep = Reporter()
    for single_sct in sct:
        state = State(
            student_data=student_data,
            solution_data=solution_data,
            sct_range=single_sct.get("range"),
            reporter=rep,
            force_diagnose=force_diagnose
        )

        SCT_CTX["Ex"].root_state = state

        try:
            exec("\n".join(single_sct.get("sct", [])), SCT_CTX)
        except TestFail as tf:
            return tf.payload

    if success_msg and isinstance(success_msg, str):
        rep.success_msg = success_msg

    return rep.build_final_payload()
