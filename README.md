# pybinhistory

*Because `pybinlog` was taken™*

`pybinhistory` reads and writes `.log` access log files, which accompany `.avb` Avid bins.  It includes data validation and convenience methods, such as the ability to "touch" a bin in one command.

In a multi-user Avid Media Composer environment, Avid will append an entry to a bin's log file each time a user writes to a bin.  With `pybinhistory`, this functionality can be mimicked programmatically. 

>[!WARNING]
>While the `.log` log file format is a very simple one, it is officially undocumented.  Use this library at your own risk -- I assume no responsibility for any damage to your
>project, loss of data, or reshoots being blatantly obvious in the final cut.

## Quick Start

### Touching A Bin

You can easily add an entry to the bin log with the `BinLog.touch()` convenience method.

```python
from binlog import BinLog

# Write default entries containing the current datetime and user info
BinLog.touch("/path/to/bin.log")      # Specify a .log path directly
BinLog.touch_bin("/path/to/bin.avb")  # Specify a .avb path.  This resolves the path to the same `bin.log` file
```

You can add custom entries by providing a [`BinLogEntry`](#binlogentry) object:

```python
from binlog import BinLog, BinLogEntry

my_cool_entry = BinLogEntry(user="me", computer="zAutomation")
BinLog.touch_bin("/path/to/bin.avb", my_cool_entry)
```

### Getting The Most Recent Entry

You can obtain the most recent bin log entry with the `BinLog.last_entry()` method.

```python
from binlog import BinLog
print(BinLog.from_bin("/path/to/bin.avb").last_entry())
```

This returns the most recent [`BinLogEntry`](#binlogentry) item in the log:

`BinLogEntry(timestamp=datetime.datetime(2023, 9, 22, 14, 8, 4), computer='zMichael', user='mj4u')`

## `BinLog`

A `BinLog` represents a... uh... bin log.  It handles reading and writing to log files, and essentially encapsulates a list of [`BinLogEntry`](#binlogentry)s.

### Reading Bin Logs

A bin log can be read from a given file path with the class method `BinLog.from_path()`

```python
from binlog import BinLog
log = BinLog.from_path("/path/to/bin.log")
```

Or, you can pass a text stream directly with the class method `BinLog.from_path()`.  This can be helpful if you're dealing with a weird text encoding, or using something other than a typical file on disk.

```python
from binlog import BinLog
with open("/path/to/bin.log", encoding="mac_roman", errors="replace") as log_handle:
  log = BinLog.from_stream(log_handle)
```

>[!NOTE]
>Unless specified by `BinLog.from_stream(encoding="somethin_else")`, `binhistory` classes assume all `.log` files are UTF-8.
>
>In testing, this has worked quite well except for a single instance of a `mac_roman` character from an ancient Avid project.

### Writing Bin Logs

Similar to [reading](#reading-bin-logs), `BinLog` can be written to a bin log with `BinLog.to_path("/path/to/bin.log")` or `BinLog.to_stream(textio_stream)`.

### Creating Bin Logs

Aside from [reading a bin log from a file](#reading-bin-logs), a new `BinLog` can be created directly with `BinLog()`, optionally passing it a list of [`BinLogEntry`](#binlogentry)s.

### Accessing `BinLogEntry`s

To access the [`BinLogEntry`](#binlogentry)s in a `BinLog`, the `BinLog` object can be directly iterated over; or a list of [`BinLogEntry`](#binlogentry)s can be retrieved via the `BinLog.entries` property.

## `BinLogEntry`

A `BinLog` contains a list of `BinLogEntry` objects.  `BinLogEntry` is really just a python [`dataclass`](https://docs.python.org/3/library/dataclasses.html) with the following fields:

* `timestamp` [[`datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects)]: Timestamp of access
* `computer` [[str](https://docs.python.org/3/library/string.html)]: Typically the hostname of the Avid that accessed the bin
* `user` [[str](https://docs.python.org/3/library/string.html)]: The Avid user who accessed the bin

### Formatting

Although `BinLog` typically handles reading and writing `BinLogEntry`s internally, `BinLogEntry` can be formatted as a typical log entry string with `.to_string()`, or read in from a log entry string with `.from_string(str)`.

## About Those Timestamps

It should be noted that a timestamp in a typical log entry file does not specify the year, but it does specify the name of the day of the week.

To derive a valid `datetime.datetime` object from this, `binhistory` methods that read existing log entries will resolve a valid year based on the file modified date of the `.log` file, working backwards until a valid day-of-the-week-name and month-day combo is found.  This typically works quite well, but if file modified dates are wildly inaccurate (for instance, working with a very old project restored from an archive that didn't retain original file timestamps), the year 
may be determined incorrectly.

Methods such as `BinLog.from_path()`, `BinLog.from_bin()`, and `BinLogEntry.from_string()` have an optional `max_year:int` argument for which you can provide the most recent year that should be considered when determining 
the correct year of the timestamp.

## See Also
- [`pybinlock`](https://github.com/mjiggidy/pybinlock)
