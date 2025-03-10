Usage
=====

The main things to know
-----------------------

:class:`.BinLog`
~~~~~~~~~~~~~~~~

:class:`.BinLog` represents an Avid bin's history log.  It behaves as a list of :class:`.BinLogEntry` objects, and can be 
used to :ref:`read <usage-reading>`, :ref:`process <usage-modifying>` and :ref:`write <usage-writing>` properly-formatted ``.log`` files.

:class:`.BinLogEntry`
~~~~~~~~~~~~~~~~~~~~~

.. _usage-entry-fields:

:class:`.BinLogEntry` is a :func:`dataclass <dataclasses.dataclass>` which represents one entry in such a log.  Per the ``.log`` file spec, 
a :class:`.BinLogEntry` has the following fields:

.. list-table::
   :header-rows: 1

   * - Field
     - Purpose
     - Default Value
   * - :attr:`.BinLogEntry.timestamp`
     - Timestamp of the modification
     - :meth:`datetime.datetime.now`
   * - :attr:`.BinLogEntry.computer`
     - Name of the machine that made the modification
     - :data:`.defaults.DEFAULT_COMPUTER`
   * - :attr:`.BinLogEntry.user`
     - Avid user profile name that made the modification
     - :data:`.defaults.DEFAULT_USER`


See :ref:`bout-dem-logs` for more information about Avid bin logs.

Creating new bin logs
---------------------

Although it's more likely you'll be working with :ref:`existing logs <usage-reading>`\, let's start by making 
one from scratch, just to get some concepts down.

.. code-block:: python
    :caption: Creating a new bin log
    :linenos:

    from binhistory import BinLog, BinLogEntry

    my_kewl_log = BinLog()

    # Add a BinLogEntry with default values
    my_kewl_log.append(BinLogEntry())

    # Add a BinLogEntry with specified `computer` and `user` values
    my_kewl_log.append(BinLogEntry(computer="zAutomation", user="otto"))

    # Let's see those entries
    for entry in my_kewl_log:
        print(entry)
    
Here's the example output:

.. code-block:: none

    BinLogEntry(timestamp=datetime.datetime(2025, 3, 9, 16, 5, 59, 112426), computer='zMichael', user='mjordan')
    BinLogEntry(timestamp=datetime.datetime(2025, 3, 9, 16, 5, 59, 112437), computer='zAutomation', user='otto')

The first entry uses default values for :attr:`timestamp <.BinLogEntry.timestamp>`\, :attr:`computer <.BinLogEntry.computer>`\, 
and :attr:`user <.BinLogEntry.user>`\. The second entry still uses the default :attr:`timestamp <.BinLogEntry.timestamp>`\, but 
has our custom :attr:`computer <.BinLogEntry.computer>` and :attr:`user <.BinLogEntry.user>` values.


Now let's see how :class:`.BinLog` would format this for the ``.log`` file, with :meth:`.BinLog.to_string`\:

.. code-block:: python
    :caption: Creating a new bin log (cont'd)
    :linenos:
    :lineno-start: 14

    print(my_kewl_log.to_string())

Output:

.. code-block:: none

    Sun Mar 09 16:05:59  Computer: thinklad        User: mjordan        
    Sun Mar 09 16:05:59  Computer: zAutomation     User: otto           
    

Great!  So let's write this out as a ``.log`` for our ``Reel 1.avb`` Avid bin with :meth:`.BinLog.to_bin`

.. code-block:: python
    :caption: Creating a new bin log (cont'd)
    :linenos:
    :lineno-start: 15

    my_kewl_log.to_bin("01_Edits/Reel 1.avb")

.. caution::

    :meth:`.BinLog.to_bin` will overwrite an existing ``.log``

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

.. admonition:: About Those Timestamps...

    The ``.log`` file spec does not specify the year in its log entry timestamp format; however it does specify the name of 
    the day of the week (Mon, Tue, Wed).

    When parsing each entry from a ``.log`` file, the year is inferred by fetching the year of 
    the file modified date of the ``.log`` as a starting point, and looking backwards through the years until a valid "day-of-the-week + 
    day-of-the-month" combo is found in the calendar.

    This seems to work quite well for active projects, but be aware of this for cases when file modified dates 
    are inaccurate --- for example, archived projects that may not have maintained their original file modification dates when they were 
    restored.
    
    In these cases, you can pass a custom year as an :class:`int` to the ``max_year`` argument to override the "file modified year" to get a more accurate date.

.. _usage-modifying:

Working with logs
-----------------

As a list
~~~~~~~~~

Since :class:`.BinLog` is a python :class:`collections.UserList` of :class:`.BinLogEntry` objects, you can do all the usual list-y kinds of things.

.. code-block:: python
    :linenos:

    from binhistory import BinLog, BinLogEntry
    from binhistory.exceptions import BinLogTypeError

    # Create a log with 5 entries
    my_log = BinLog([BinLogEntry(), BinLogEntry(), BinLogEntry(), BinLogEntry(), BinLogEntry()])

    # Get the third entry
    some_entry = my_log[2]

    # Modify the third entry
    my_log[2] = some_entry.copy_with(computer="zSomething")

    # Add a couple more entries
    my_log.extend([BinLogEntry(computer="zNew"), BinLogEntry(user="Another")])

    # Count the entries
    print(f"my_log has {len(my_log)} entries.")

    # Note: `BinLog` will only accept `BinLogEntry`s
    try:
        my_log.append("Heehee oops")
    except BinLogTypeError as e:
        print(f"This didn't work: {e}")



Convenience methods
~~~~~~~~~~~~~~~~~~~

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
    
    # Get all the Avid bins in a project
    for bin_path in pathlib.Path("/Volumes/Important Avid Project/").rglob("*.avb"):

        if bin_path.name.startswith("."):
            # Skip dotfiles
            continue

        try:
            # Read the log for this bin
            log = BinLog.from_bin(bin_path)
        except BinLogNotFoundError:
            # Skip bins without logs
            continue
        
        if suspect in log.computers():
            print(f"{suspect} made changes to {bin_path}!")

.. _usage-writing:

Working with log entries
------------------------

As mentioned earlier, a :class:`.BinLogEntry` object is a :func:`dataclass <dataclasses.dataclass>` that represents a single log entry.  
It comes with :ref:`default values <usage-entry-fields>` set for each of the fields, so let's check that out first:

.. code-block:: python
    :linenos:

    from binlog import BinLogEntry

    print(BinLogEntry())

Output:

.. code-block:: none

    BinLogEntry(timestamp=datetime.datetime(2025, 3, 8, 15, 27, 25, 76253), computer='zMichael', user='mjordan')

Nice!  We see :attr:`timestamp <.BinLogEntry.timestamp>` defaults to the current datetime.  :attr:`computer <.BinLogEntry.computer>` 
defaults to the hostname of my machine, and :attr:`user <.BinLogEntry.user>` defaults to the username executing the script.

.. note::
    
    Those default values can be changed, on a per-script basis, by modifying the constants defined in the :mod:`.defaults` module.

Now, those first two are in line with the data Avid would use for the log entry under normal circumstances.  But 
for :attr:`user <.BinLogEntry.user>`\, typically Avid would use the name of the current Avid user profile.  So let's specify 
that field:

.. code-block:: python
    :linenos:

    from binlog import BinLogEntry

    print(BinLogEntry(user="MJ 2023.12.2"))

Output:

.. code-block:: none

    BinLogEntry(timestamp=datetime.datetime(2025, 3, 8, 15, 28, 29, 47132), computer='zMichael', user='MJ 2023.12.2')

Cool.  This matches exactly what Avid would normally use for a bin entry.

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