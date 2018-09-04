# import pytest
# import re
# from copy import deepcopy
# from utils import Identity, Mutation, try_exercise, compose
#
#
## Fixtures
# @pytest.fixture()
# def solution_data():
#    return {
#        "values": [[1, 1, 1], [1, 52, 8]],
#        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
#    }
#
#
## Tests
# @pytest.mark.parametrize(
#    "trans, sct_range, message_shown, sct_function, sct_args",
#    [
#        (Identity(), "A1", False, "check_formula", None),
#        (Mutation(["formulas", 0, 0], 0), "A1", True, "check_formula", None),
#        (Mutation(["formulas", 0, 0], 0), "B1", False, "check_formula", None),
#        (Identity(), "A1", False, "check_regex", 'pattern=""'),
#        (
#            Mutation(["formulas", 0, 0], 0),
#            "A1",
#            True,
#            "check_regex",
#            'pattern="testtest"',
#        ),
#        (Mutation(["formulas", 0, 0], 0), "B1", False, "check_regex", 'pattern=""'),
#        (Identity(), "A1", False, "check_value", None),
#        (Mutation(["values", 0, 0], 0), "A1", True, "check_value", None),
#        (Mutation(["values", 0, 0], 0), "B1", False, "check_value", None),
#    ],
# )
# def test_overwrite_message(
#    solution_data, trans, sct_range, message_shown, sct_function, sct_args
# ):
#    user_data = trans(deepcopy(solution_data))
#    expected_message = "Try again!"
#    full_sct = f"{sct_function}(message='{expected_message}')"
#    if sct_args is not None:
#        full_sct = f"{full_sct[:-1]}, {sct_args})"
#    sct = [{"range": sct_range, "sct": [full_sct]}]
#    real_message = try_exercise(solution_data, user_data, sct).get("message")
#    if not (message_shown):
#        assert real_message == None or not (real_message == expected_message)
#    else:
#        assert real_message == expected_message
#
#
# @pytest.mark.parametrize(
#    "trans, sct_range, suggestion_shown, sct_function, sct_args",
#    [
#        (Identity(), "A1", False, "check_formula", None),
#        (Mutation(["formulas", 0, 0], 0), "A1", True, "check_formula", None),
#        (Mutation(["formulas", 0, 0], 0), "B1", False, "check_formula", None),
#        (Identity(), "A1", False, "check_regex", 'pattern=""'),
#        (
#            Mutation(["formulas", 0, 0], 0),
#            "A1",
#            True,
#            "check_regex",
#            'pattern="testtest"',
#        ),
#        (Mutation(["formulas", 0, 0], 0), "B1", False, "check_regex", 'pattern=""'),
#        (Identity(), "A1", False, "check_value", None),
#        (Mutation(["values", 0, 0], 0), "A1", True, "check_value", None),
#        (Mutation(["values", 0, 0], 0), "B1", False, "check_value", None),
#    ],
# )
# def test_overwrite_suggestion(
#    solution_data, trans, sct_range, suggestion_shown, sct_function, sct_args
# ):
#    user_data = trans(deepcopy(solution_data))
#    suggestion = "Try again!"
#    full_sct = f"{sct_function}(message='{suggestion}')"
#    if sct_args is not None:
#        full_sct = f"{full_sct[:-1]}, {sct_args})"
#    sct = [{"range": sct_range, "sct": [full_sct]}]
#    message = try_exercise(solution_data, user_data, sct).get("message")
#    if not (suggestion_shown):
#        assert message == None or not (message.endswith(suggestion))
#    else:
#        assert message.endswith(suggestion)
#
#
# @pytest.mark.parametrize(
#    "trans, sct_range, sct_function",
#    [
#        (Mutation(["values", 0, 0], None), "A1", "check_value"),
#        (
#            compose(
#                Mutation(["values", 0, 0], None), Mutation(["formulas", 0, 0], None)
#            ),
#            "A1",
#            "check_formula",
#        ),
#        (
#            compose(
#                Mutation(["values", 0, 0], None), Mutation(["formulas", 0, 0], None)
#            ),
#            "A1",
#            "check_regex(pattern='testtest')",
#        ),
#        (Identity(), "Z100", "check_value"),
#        (Identity(), "Z100", "check_formula"),
#        (Identity(), "Z100", "check_regex(pattern='testtest')"),
#    ],
# )
# def test_empty_cell(solution_data, trans, sct_range, sct_function):
#    user_data = trans(deepcopy(solution_data))
#    sct = [{"range": sct_range, "sct": [sct_function]}]
#    message = try_exercise(solution_data, user_data, sct).get("message")
#    assert message.startswith(f"Please fill in `{sct_range}`")
