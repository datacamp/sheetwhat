import pytest
from sheetwhat.test_exercise import test_exercise as te


@pytest.mark.parametrize(
    "sct_range, sct, success",
    [
        ("A1", "Ex().has_code('A')", True),
        ("B1", "Ex().has_code('A')", False),
        ("A1", "Ex().has_equal_value()", True),
        ("B1", "Ex().has_equal_value()", False),
        ("A1", "Ex().has_equal_formula()", True),
        ("B1", "Ex().has_equal_formula()", False),
    ],
)
def test_full(sct_range, sct, success):
    result = te(
        sct=[{"range": sct_range, "sct": [sct]}],
        student_data={"values": [["A", "B"]], "formulas": [["=A1", "=B1"]]},
        solution_data={"values": [["A", "A"]], "formulas": [["=A1", "=A1"]]},
    )
    assert result["correct"] == success


def test_empty():
    result = te(sct=[], student_data={}, solution_data={})
    assert result["correct"]


@pytest.mark.parametrize(
    "success_msg, patt",
    [
        (None, "Great work!"),
        ("", "Great work!"),
        ("you `rock`", "you <code>rock</code>"),
    ],
)
def test_success_msg(success_msg, patt):
    result = te(sct=[], student_data={}, solution_data={}, success_msg=success_msg)
    assert result["correct"]
    assert result["message"] == patt


@pytest.mark.parametrize(
    "sct, student_data, solution_data", [({}, [], []), ([], [], []), ([], {}, [])]
)
def test_malformed(sct, student_data, solution_data):
    with pytest.raises(AssertionError):
        te(sct, student_data, solution_data)


def test_format_string_messaging():
    sct_range = "A1"
    sct = 'Ex().check_operator(operator="<", missing_msg="Check cell `{range}` again.")'
    result = te(
        sct=[{"range": sct_range, "sct": [sct]}],
        student_data={"values": [["A", "B"]], "formulas": [["=A1", "=B1"]]},
        solution_data={"values": [["A", "A"]], "formulas": [["=A1", "=A1"]]},
    )
    assert result["message"] == "Check cell <code>A1</code> again."
