Glossary
--------

This article lists some example solutions. For each of these solutions, an SCT
is included, as well as some example student submissions that would pass and fail. In all of these, a submission that
is identical to the solution will evidently pass.

.. note:: 

    These SCT examples are not golden bullets that are perfect for your situation.
    Depending on the exercise, you may want to focus on certain parts of a statement, or be 
    more accepting for different alternative answers.

All these examples come from the `Intro to Shell for Data Science <https://www.datacamp.com/courses/introduction-to-shell-for-data-science>`_
and `Introduction to Git for Data Science <https://www.datacamp.com/courses/introduction-to-git-for-data-science>`_ courses. You can have a look at their
respective GitHub sources `here <https://github.com/datacamp/courses-intro-to-unix-shell>`_ and
`here <https://github.com/datacamp/courses-intro-to-git>`_, respectively.

Checking the current directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # solution command
    cd test

.. code::

    # sct
    Ex().has_cwd('/home/repl/test')


Checking the ``ls`` statement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # solution command
    ls

.. code::

    # sct
    Ex().check_correct(
        has_cwd('/home/repl')
        has_expr_output()
    )

Checking whether a directory exists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # solution command
    mdkir /home/repl/test

.. code::

    # sct
    Ex().has_dir('/home/repl/test')


Checking command output
~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: shell

    # solution command
    echo 'this is a printout!'

.. code::

    # sct
    Ex().has_output(r'this\\s+is\\s+a\\s+print\\s*out')

.. code-block:: shell

    # Submissions that would pass:
    echo 'this   is a print out'
    test='this is a printout!' && echo $test

    # Submissions that would fail:
    echo 'this is a wrong printout'

Checking contents of a file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # solution command
    echo hello > test.txt

.. code::

    # sct
    Ex().check_file('/home/repl/test.txt').multi(
        # check that file contains hello or hi
        has_code(r'hello|hi'),
        # check that file does not contain goodbye
        check_not(has_code('goodbye'),
                  incorrect_msg="meaningful error message")
    )

Git: check branch
~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # solution command (while in the test git repo)
    git checkout make-change

.. code::

    Ex().multi(
        has_cwd('/home/repl/test'),
        has_expr_output(expr='git rev-parse --abbrev-ref HEAD | grep make-change',
                        output='make-change', strict=True,
                        incorrect_msg=meaningful message")
    )

Git: check that file was staged
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    # solution command (while in the test git repo)
    git add test.txt

.. code::

    # sct
    Ex().multi(
        has_cwd('/home/repl/test')
        has_expr_output(expr="git diff --name-only --staged | grep test.txt",
                        output="test.txt", strict=True,
                        incorrect_msg="meaningful message")
    )
