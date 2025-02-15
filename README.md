# pybinblog

`pybinlog` reads and writes `.log` access log files, which accompany `.avb` Avid bins.  It includes data validation and convenience methods, such as the ability to "touch" a bin in one command.

## Convenience Methods

### Touching A Bin

You can easily add an entry to the bin log with the `BinLog.touch()` convenience method.

```python
from binlog import BinLog
BinLog.touch("/path/to/bin.log", computer="avidmac", user="aviduser")
```

### Getting The Most Recent Entry

You can obtain the most recent bin log entry with the `BinLog.last_entry()` convenience method.

```python
from binlog import BinLog
print(BinLog.last_entry("/path/to/bin.log"))
```

This returns the most recent [`BinLogEntry`](#binlogentry) item in the log:

`BinLogEntry(timestamp=datetime.datetime(2023, 9, 22, 14, 8, 4), computer='zMichael', user='mj4u')`

## Reading Bin Logs

A bin log can be read from a given file path with the class method `BinLog.from_path()`

```python
from binlog import BinLog
log = BinLog.from_path("/path/to/bin.log")
```

Or, you can pass a text stream directly with the class method `BinLog.from_path()`.  This can be helpful if you're dealing with a weird text encoding, or outputting to something other than a typical file.

```python
from binlog import BinLog
with open("/path/to/bin.log", encoding="mac_roman", errors="replace") as log_handle:
  log = BinLog.from_stream(log_handle)
```

## Writing Bin Logs

Similar to [reading](#reading-bin-logs), `BinLog` can be written to a bin log with `BinLog.to_path("/path/to/bin.log")` or `BinLog.to_stream(textio_stream)`.

## `BinLogEntry`

A `BinLog` contains a list of `BinLogEntry` objects.  `BinLogEntry` is really just a python [`dataclass`](https://docs.python.org/3/library/dataclasses.html) with the following fields:

* `timestamp` [[`datetime`](https://docs.python.org/3/library/datetime.html#datetime-objects)]: Timestamp of access
* `computer` [[str](https://docs.python.org/3/library/string.html)]: Typically the hostname of the Avid that accessed the bin
* `user` [[str](https://docs.python.org/3/library/string.html)]: The Avid user who accessed the bin

### Formatting

Although `BinLog` typically handles reading and writing `BinLogEntry`s internally, `BinLogEntry` can be formatted as a typical log entry string with `.to_string()`, or read in from a log entry string with `.from_string(str)`.
