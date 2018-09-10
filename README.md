# sheetwhat

[![Build Status](https://travis-ci.org/datacamp/sheetwhat.svg?branch=master)](https://travis-ci.org/datacamp/sheetwhat)
[![codecov](https://codecov.io/gh/datacamp/sheetwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/sheetwhat)
[![PyPI version](https://badge.fury.io/py/sheetwhat.svg)](https://badge.fury.io/py/sheetwhat)

`sheetwhat` enables you to write Submission Correctness Tests (SCTs) for interactive Spreadsheet exercises on DataCamp.

- If you are new to teaching on DataCamp, check out https://authoring.datacamp.com.
- If you want to learn what SCTs are and how they work, visit [this article](https://authoring.datacamp.com/courses/exercises/technical-details/sct.html) specifically.
- For a complete overview of all functionality inside `sheetwhat` and articles about what to use when, consult https://sheetwhat.readthedocs.io.

## Installing

```
pip install sheetwhat
```

## Demo

Sheetwhat is typically used in a web application, but you can also experiment with its functions on your local machine.
SCT functions that fail will throw a `TestFail` error.

```python
# Setup: make all checking functions available
from sheetwhat.sct_syntax import SCT_CTX
globals().update(SCT_CTX)

# Setup: set up state with student data, solution data and SCT range
from sheetwhat.State import State
from protowhat.Reporter import Reporter
Ex.root_state = State(
    {'values': [["a", "a"]], "formulas": [["=B1"]]},
    {'values': [["b", "b"]], "formulas": [["=B1"]]},
    "A1",
    Reporter()
)

# Experiment interactively with SCTs
# Passes, as formulas at A1 match
Ex().has_equal_formula()

# Fails, as values at A1 do not match
Ex().has_equal_value()
```

## Testing

```
pip install -r requirements.txt
pip install -e .
pytest
```
