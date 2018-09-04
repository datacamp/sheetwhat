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
