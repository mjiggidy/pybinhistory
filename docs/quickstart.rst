Getting started
===============

Once you have :doc:`installed <installation>` the ``pybinhistory`` package, you can now import 
the :mod:`binhistory` module.

.. code-block:: python
    :linenos:

    import binhistory

Quick 'n' dirty
---------------

These should get you up and running quickly, but see :doc:`usage` for details.

Read an Avid bin's log
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :linenos:

    from binhistory import BinLog

    log = BinLog.from_bin("01_EDITS/Reel 1.avb")
    for entry in log:
        print(entry)

:class:`.BinLog` behaves as a list of :class:`.BinLogEntry` objects.  Example Output:

.. code-block:: none

    BinLogEntry(timestamp=datetime.datetime(2024, 8, 29, 17, 27, 12), computer='zJoy', user='joyjoy')
    BinLogEntry(timestamp=datetime.datetime(2024, 8, 30, 14, 16, 42), computer='zMichael', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2025, 2, 22, 18, 5, 43), computer='zTimmy', user='user')
    BinLogEntry(timestamp=datetime.datetime(2025, 4, 10, 10, 34, 59), computer='zTootsie_LA', user='toot')

Append an entry to a bin's log
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:

   from binhistory import BinLog, BinLogEntry

   BinLog.touch_bin("01_EDITS/Reel 1.avb", BinLogEntry(computer="zAutomation"))

Since :class:`.BinLogEntry` has sane default values, :attr:`.BinLogEntry.timestamp` defaults to the current time, 
and :attr:`.BinLogEntry.user` defaults to the current username executing the script.