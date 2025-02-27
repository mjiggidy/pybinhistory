"""
Given the path to an Avid bin, append an entry via the `BinLog.touch()` convenience method
"""

from binhistory import BinLog
import sys

BinLog.touch_bin(sys.argv[1])