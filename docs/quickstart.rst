Getting started
===============

Once you have :doc:`installed <installation>` the ``pybinhistory`` package, you can now import 
the :mod:`binhistory` module.

.. code-block:: python

    import binhistory

Quick 'n' dirty
---------------

These should get you up and running quickly, but see :doc:`usage` for details.

Read an Avid bin's log
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from binhistory import BinLog

    log = BinLog.from_bin("01_EDITS/Reel 1.avb")
    for entry in log:
        print(entry)

:class:`binhistory.BinLog` behaves as a list of :class:`binhistory.BinLogEntry` objects.  Example Output:

.. code-block:: bash

    BinLogEntry(timestamp=datetime.datetime(2024, 8, 29, 17, 27, 12), computer='zJoy', user='joyjoy')
    BinLogEntry(timestamp=datetime.datetime(2024, 8, 30, 14, 16, 42), computer='zMichael_LA', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2025, 2, 22, 18, 5, 43), computer='zTimmy', user='user')
    BinLogEntry(timestamp=datetime.datetime(2025, 4, 10, 10, 34, 59), computer='zTootsie_LA', user='toot')

Append an entry to a bin's log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from binhistory import BinLog, BinLogEntry

   BinLog.touch_bin("01_EDITS/Reel 1.avb", BinLogEntry(computer="zAutomation"))

Since :class:`binhistory.BinLogEntry` has sane default values, ``timestamp`` reflects the current time, 
and ``user`` reflects the current username executing the script.