sheetwhat
=========

[![Build Status](https://travis-ci.org/datacamp/sheetwhat.svg?branch=master)](https://travis-ci.org/datacamp/sheetwhat)
[![codecov](https://codecov.io/gh/datacamp/sheetwhat/branch/master/graph/badge.svg)](https://codecov.io/gh/datacamp/sheetwhat)
[![PyPI version](https://badge.fury.io/py/sheetwhat.svg)](https://badge.fury.io/py/sheetwhat)

`sheetwhat` enables you to write Submission Correctness Tests (SCTs) for interactive Spreadsheet exercises on DataCamp.

- If you are new to teaching on DataCamp, check out https://authoring.datacamp.com.
- If you want to learn what SCTs are and how they work, visit [this article](https://authoring.datacamp.com/courses/exercises/technical-details/sct.html) specifically.
- For a complete overview of all functionality inside `sheetwhat` and articles about what to use when, consult https://sheetwhat.readthedocs.io.

Installing
----------

```
pip install sheetwhat
```

Testing
-------

```
pip install -r requirements.txt
pip install -e .
pytest
```