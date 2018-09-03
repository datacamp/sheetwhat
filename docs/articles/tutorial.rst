Tutorial
--------

sheetwhat uses the ``.`` to 'chain together' SCT functions. Every chain starts with the ``Ex()`` function call, which holds the exercise state.
This exercise state contains all the information that is required to check if an exercise is correct, which are:

+ the student submission and the solution as text, and their corresponding parse trees.
+ the result of running the solution, as an ANSI-formatted string.
+ the result of running the student's query, as an ANSI-formatted string.
+ the errors that running the student's query generated, if any.

As SCT functions are chained together with ``.``, the ``Ex()`` exercise state is copied and adapted into 'sub states' to zoom in on particular parts of the state.
Before this theory blows your brains out, some examples will be included in this tutorial soon.
