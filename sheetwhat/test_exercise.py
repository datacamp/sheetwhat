from protowhat.Test import TestFail
from protowhat.Reporter import Reporter

from sheetwhat.sct_syntax import SCT_CTX
from sheetwhat.State import State


def test_exercise(sct, student_data, solution_data):
    """
    """

    for single_sct in sct:
        state = State(
            student_data=student_data,
            solution_data=solution_data,
            sct_range=single_sct.get("range"),
            reporter=Reporter(),
        )

        SCT_CTX["Ex"].root_state = state

        try:
            exec("\n".join(single_sct.get("sct", [])), SCT_CTX)
        except TestFail as tf:
            return tf.payload

    return state.reporter.build_final_payload()
