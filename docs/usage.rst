Usage
=====

The main things to know
-----------------------

:class:`.BinLog` represents a bin ``.log``\.  It behaves as a list of :class:`.BinLogEntry` entries:

.. autoclass:: binhistory.BinLog
    :no-members:
    :noindex:

:class:`.BinLogEntry` is a :func:`dataclass <dataclasses.dataclass>` representing a 
single entry in a log:

.. autoclass:: binhistory.BinLogEntry
    :no-members:
    :noindex:

Reading existing logs
---------------------

:class:`.BinLog` can read an Avid bin's log with :meth:`.BinLog.from_bin`:

.. automethod:: binhistory.BinLog.from_bin
    :no-index:

If no ``.log`` file exists for the given bin, :class:`.exceptions.BinLogNotFoundError` is raised.

So to read the log for the Avid bin ``01_Edits/Reel 1.avb``:

.. code-block:: python

    from binhistory import BinLog
    from binhistory.exceptions import BinLogNotFoundError

    bin_path = "01_EDITS/Reel 1.avb"
    try:
        log = BinLog.from_bin(bin_path)
    except BinLogNotFoundError:
        print(f"No log file exist for {bin_path}")
        return
    
    for entry in log:
        print(entry)

Here's an example output from an Avid bin that has been modified four times:

.. code-block:: bash

    BinLogEntry(timestamp=datetime.datetime(2024, 8, 29, 17, 27, 12), computer='zJoy', user='joyjoy')
    BinLogEntry(timestamp=datetime.datetime(2024, 8, 30, 14, 10, 16), computer='zMichael_LA', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2024, 8, 30, 14, 16, 42), computer='zMichael_LA', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2025, 2, 22, 18, 5, 43), computer='zTimmy', user='user')

Working with logs
-----------------

As a list
^^^^^^^^^

*Something something*

Convenience methods
^^^^^^^^^^^^^^^^^^^

Extents
~~~~~~~

Often you may be interested in only the earliest or the last entry in the log.  Well, buddy, 
you're not gonna believe this:

.. automethod:: binhistory.BinLog.earliest_entry
    :noindex:

.. automethod:: binhistory.BinLog.latest_entry
    :noindex:

These methods will return :obj:`None` if the :class:`.BinLog` has no :class:`.BinLogEntry`\s.

.. code-block:: python

    from binhistory import BinLog
    from binhistory.exceptions import BinLogNotFoundError

    bin_path = "01_EDITS/Reel 1.avb"
    try:
        latest_entry = BinLog.from_bin(bin_path).latest_entry()
    except BinLogNotFoundError:
        print(f"No log file exist for {bin_path}")
        return
    
    if not latest_entry:
        # Sometimes a .log file exists, but is empty
        print(f"Empty log for {bin_path}")
        return
    
    print(f"{bin_path} was last modified by {latest_entry.computer} on {latest_entry.timestamp}")

Example output:

.. code-block:: bash

    01_EDITS/Reel 1.avb was last modified by zTimmy on 2025-02-22 18:05:43

Stats
~~~~~

You can also get lists of unique field values in a log with the following:

.. automethod:: binhistory.BinLog.computers
        :noindex:

.. automethod:: binhistory.BinLog.users
        :noindex:

.. automethod:: binhistory.BinLog.timestamps
        :noindex:

As an example, let's get a list of all the bins that have been recently modified by 
my ``zMichael_LA`` machine.  Then we can blame me for things!

.. code-block:: python
    
    import pathlib
    from binhistory import BinLog
    from binhistory.exceptions import BinLogNotFoundError

    suspect = "zMichael"

    for bin_path in pathlib.Path("/Volumes/Important Avid Project/").rglob("*.avb"):

        if bin_path.name.startswith("."):
            # Skip dotfiles
            continue

        try:
            log = BinLog.from_bin(bin_path)
        except BinLogNotFoundError:
            # Skip bins without logs
            continue
        
        if suspect in log.computers():
            print(f"{suspect} made changes to {bin_path}!")

Writing logs
============

:meth:`.BinLog.touch_bin` will append 