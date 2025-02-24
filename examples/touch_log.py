"""
Given the path to a log file, append an entry via the `BinLog.touch()` convenience method
"""

from binlog import BinLog, BinLogEntry
import sys

BinLog.touch(sys.argv[1], BinLogEntry())