Tutorial
--------

sheetwhat uses the ``.`` to 'chain together' SCT functions. Every chain starts with the ``Ex()`` function call, which holds the exercise state.
This exercise state contains all the information that is required to check if an exercise is correct, which are:

+ the student's spreadsheet (both the formulas and the resulting values),
+ the solution's spreadsheet (both the formulas and the resulting values),
+ the range for which the SCT is specified.

As SCT functions are chained together with ``.``, the ``Ex()`` exercise state is copied and adapted into 'sub states' to zoom in on particular parts of the state.
Before this theory blows your brains out, some examples will be included in this tutorial soon.
