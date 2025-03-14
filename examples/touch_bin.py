"""
Given the path to an Avid bin, append an entry via the `BinLog.touch()` convenience method
"""

from binhistory import BinLog, exceptions
import sys

if not len(sys.argv) > 1 or not sys.argv[1].lower().endswith(".avb"):
	sys.exit("Usage: {__file__} avidbin.avb")

try:
	BinLog.touch_bin(sys.argv[1], missing_bin_ok=False)
except exceptions.BinNotFoundError:
	sys.exit(f"Avid bin not found: {sys.argv[1]}")