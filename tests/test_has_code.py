import pytest
from copy import deepcopy
from helper import Identity, Mutation, compose, setup_state, verify_success
from sheetwhat.checks import has_code

# Fixtures
@pytest.fixture()
def user_data_seed():
    return {
        "values": [[1, 1, 1], [1, 52, 8]],
        "formulas": [["=0+1", 1, 1], ["=1+0", "=52", 8]],
    }


# Tests
@pytest.mark.parametrize(
    "trans, sct_range, pattern, correct",
    [
        (Identity(), "A1", "=0", True),
        (Identity(), "A1:A2", "=", True),
        (Mutation(["formulas", 0, 0], "= 1 + 0"), "A1", "=1+0", False),
        (Mutation(["values", 1, 1], "test"), "B2", "test", False),
        (Mutation(["formulas", 1, 1], "test"), "B2", "test", True),
        (Mutation(["formulas", 0, 1], "testtesttest"), "B1", "^(?:test)+$", True),
        (Mutation(["formulas", 0, 1], ""), "B1", "^(?:test)+$", False),
        (
            compose(
                Mutation(["formulas", 0, 0], "=0+0"),
                Mutation(["formulas", 0, 1], "=1+0"),
                Mutation(["formulas", 1, 0], "=0+1"),
                Mutation(["formulas", 1, 1], "=1-1"),
                Mutation(["values", 0, 0], 0),
                Mutation(["values", 0, 1], 1),
                Mutation(["values", 1, 0], 1),
                Mutation(["values", 1, 1], 2),
            ),
            "A1:B2",
            "1|0 +|- 1|0",
            True,
        ),
    ],
)
def test_check_regex(user_data_seed, trans, sct_range, pattern, correct):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data, sct_range)
    with verify_success(correct):
        has_code(s, pattern)


@pytest.mark.debug
@pytest.mark.parametrize(
    "trans, sct_range, pattern, correct",
    [
        (Mutation(["formulas", 0, 0], "dees+"), "A1", "dees+", True),
        (Mutation(["formulas", 0, 0], "deesssss"), "A1", "dees+", False),
        (Mutation(["formulas", 0, 0], "dees"), "A1", "dees+", False),
    ],
)
def test_check_regex_fixed(user_data_seed, trans, sct_range, pattern, correct):
    user_data = trans(deepcopy(user_data_seed))
    s = setup_state(user_data, user_data, sct_range)
    with verify_success(correct):
        has_code(s, pattern, fixed=True)
