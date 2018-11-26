import importlib
import pytest
from tests.helper import setup_state
from protowhat.Test import TestFail as TF
from sheetwhat.checks import *


@pytest.mark.parametrize(
    "field, field_msg, patt",
    [
        ("values", "value", "Please fill in a value in `B1`."),
        ("formulas", "formula", "Please fill in a formula in `B1`."),
    ],
)
def test_check_range(field, field_msg, patt):
    s = setup_state(
        {"values": [[1]], "formulas": [["=1"]]},
        {"values": [[1, 2]], "formulas": [["=1"]]},
        "B1",
    )
    with pytest.raises(TF, match=patt):
        check_range(s, field, field_msg)


def test_has_code():
    user_data = {"formulas": [["missing"]]}
    s = setup_state(user_data, user_data, "A1")
    with pytest.raises(TF, match=r"In cell `A1`, did you use the correct formula\?"):
        has_code(s, "something")


def test_check_function():
    user_data = {"formulas": [["SUM(B1)"]]}
    s = setup_state(user_data, user_data, "A1")
    with pytest.raises(
        TF, match=r"In cell `A1`, did you use the `AVERAGE\(\)` function\?"
    ):
        check_function(s, name="AVERAGE")


def test_check_operator():
    user_data = {"formulas": [["=1 + 2"]]}
    s = setup_state(user_data, user_data, "A1")
    with pytest.raises(TF, match=r"In cell `A1`, did you use the `/` operator\?"):
        check_operator(s, operator="/")


def test_has_equal_value():
    s = setup_state({"values": [[1]]}, {"values": [[2]]}, "A1")
    with pytest.raises(TF, match=r"The value at `A1` is not correct."):
        has_equal_value(s)


def test_has_equal_formula():
    s = setup_state({"formulas": [["=1"]]}, {"formulas": [["=2"]]}, "A1")
    with pytest.raises(TF, match=r"In cell `A1`, did you use the correct formula\?"):
        has_equal_formula(s)


def test_has_equal_reference():
    s = setup_state({"formulas": [["=A1"]]}, {"formulas": [["=B1"]]}, "A1")
    with pytest.raises(TF, match=r"In cell `A1`, did you use the reference `B1`\?"):
        has_equal_references(s)


def test_has_equal_reference_bas():
    s = setup_state({"formulas": [["=$A$1"]]}, {"formulas": [["=$B$1"]]}, "A1")
    with pytest.raises(
        TF, match=r"In cell `A1`, did you use the absolute reference `\$B\$1`\?"
    ):
        has_equal_references(s, absolute=True)


def test_format_string_messaging():
    s = setup_state(
        {"values": [["A", "B"]], "formulas": [["=A1", "=B1"]]},
        {"values": [["A", "A"]], "formulas": [["=A1", "=A1"]]},
        "A1",
    )
    with pytest.raises(TF, match=r"Check cell `A1` again."):
        check_operator(s, operator="<", missing_msg="Check cell `{range}` again.")
