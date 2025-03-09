Usage
=====

The main things to know
-----------------------

:class:`.BinLog`
~~~~~~~~~~~~~~~~

:class:`.BinLog` represents an Avid bin's history log.

.. autoclass:: binhistory.BinLog
    :no-members:
    :noindex:

:class:`.BinLog` behaves as a list of :class:`.BinLogEntry` objects.  It can be used to :ref:`read <usage-reading>`, 
:ref:`process <usage-modifying>` and :ref:`write <usage-writing>` properly-formatted ``.log`` files.

:class:`.BinLogEntry`
~~~~~~~~~~~~~~~~~~~~~

:class:`.BinLogEntry` is a :func:`dataclass <dataclasses.dataclass>` which represents one entry in such a log.

.. autoclass:: binhistory.BinLogEntry
    :no-members:
    :noindex:


Per the ``.log`` file spec, a :class:`.BinLogEntry` has fields for the :attr:`timestamp <.BinLogEntry.timestamp>` of the 
entry, the :attr:`computer <.BinLogEntry.computer>` (host name) of the machine that made the modification, and the 
:attr:`user <.BinLogEntry.user>` (Avid user profile name) that was operating that computer.

See :ref:`bout-dem-logs` for more information about Avid bin logs.

.. _usage-reading:

Reading existing logs
---------------------

:class:`.BinLog` can read an Avid bin's log with :meth:`.BinLog.from_bin`:

.. automethod:: binhistory.BinLog.from_bin
    :no-index:

If no ``.log`` file exists for the given bin, :class:`.exceptions.BinLogNotFoundError` is raised.

So to read the log for the Avid bin ``01_Edits/Reel 1.avb``:

.. code-block:: python
    :linenos:

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

.. code-block:: none

    BinLogEntry(timestamp=datetime.datetime(2024, 8, 29, 17, 27, 12), computer='zJoy', user='joyjoy')
    BinLogEntry(timestamp=datetime.datetime(2024, 8, 30, 14, 10, 16), computer='zMichael', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2024, 8, 30, 14, 16, 42), computer='zMichael', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2025, 2, 22, 18, 5, 43), computer='zTimmy', user='user')

.. admonition:: A Gentle Word Of Caution

    The ``.log`` file format does not specify years in its log entry timestamps; however it does specify the name of 
    the day of the week.

    When parsing entries from a ``.log`` file, a best guess of the year is made by starting with the year of 
    the file modified date, and looking backwards through the years until a valid day-of-the-week + 
    day-of-the-month combo is found.

    This seems to work quite well for active projects, but be aware of this for cases when file modified dates 
    are inaccurate --- for example, archived projects that may have adopted modern modification dates when they were 
    restored.
    
    In these cases, you can pass a custom year as an :class:`int` to the ``max_year`` argument to override the "file modified year" to get a more accurate date.

.. _usage-modifying:

Working with logs
-----------------

As a list
~~~~~~~~~

*Something something*

Convenience methods
~~~~~~~~~~~~~~~~~~~

Extents
^^^^^^^

Often you may be interested in only the earliest or the last entry in the log.  Well, buddy, 
you're not gonna believe this:

.. automethod:: binhistory.BinLog.earliest_entry
    :noindex:

.. automethod:: binhistory.BinLog.latest_entry
    :noindex:

These methods will return :obj:`None` if the :class:`.BinLog` has no :class:`.BinLogEntry`\s.

.. code-block:: python
    :linenos:

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

.. code-block:: none

    01_EDITS/Reel 1.avb was last modified by zTimmy on 2025-02-22 18:05:43

Stats
^^^^^

You can also get lists of unique field values in a log with the following:

.. automethod:: binhistory.BinLog.computers
        :noindex:

.. automethod:: binhistory.BinLog.users
        :noindex:

.. automethod:: binhistory.BinLog.timestamps
        :noindex:

As an example, let's get a list of all the bins that have been recently modified by 
my ``zMichael`` machine.  Now we can blame me for things!

.. code-block:: python
    :linenos:
    
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

.. _usage-writing:

Writing logs
------------

The :class:`.BinLog` class knows how to write properly-formatted ``.log`` files, and provides a couple 
of ways of doing so.

.. note::
    
    While :class:`.BinLog` may contain any number of :class:`.BinLogEntry` objects in any order, the 
    resulting ``.log`` file will always be output with a maximum of :data:`.defaults.MAX_ENTRIES` of the most recent entries, 
    sorted according to the :attr:`.BinLogEntry.timestamp` field.

Touching a bin
~~~~~~~~~~~~~~

:meth:`.BinLog.touch_bin` is a class method which appends an entry to the log of a given Avid bin.  It's designed to be 
a quick thing you can call with no arguments, but you may optionally provide a custom :class:`.BinLogEntry`

If no ``.log`` exists for the Avid bin, one will be created.

.. automethod:: binhistory.BinLog.touch_bin
    :noindex:

In this example, imagine it's... oh I don't know... 3:27pm on March 8, 2025.

.. code-block:: python
    :linenos:
    
    from binhistory import BinLog

    bin_path = "01_Edits/Reel 1.avb"

    # Add a default BinLogEntry to the log
    BinLog.touch_bin(bin_path)

    # Now let's see that log
    print(BinLog.from_bin(bin_path).latest_entry())

The latest entry shows my touch:

.. code-block:: none

    BinLogEntry(timestamp=datetime.datetime(2025, 3, 8, 15, 27, 25, 76253), computer='zMichael', user='mjordan')