"""
For a given Avid bin containing sequences, resolve who last modified each sequence

NOTE: This example requires the `pyavb` package.  Install via `pip install pyavb`
NOTE: This example requires the `pybinlock` package.  Install via `pip install pybinlock`
"""

import sys, pathlib, datetime
import binhistory

USAGE = f"Usage: {pathlib.Path(__file__).name} avidbin.avb"

try:
	import avb, binlock
except ImportError:
	print("`pyavb` and `pybinlock` packages are required for this example, but was not found.  Please `pip install` them before using", file=sys.stderr)
	sys.exit(1)

def get_log_entry_for_timestamp(log:binhistory.BinLog, timestamp:datetime.datetime) -> binhistory.BinLog:
	"""Get the closest log entry for a given timestamp"""

	last = None
	for log_entry in log:
		if log_entry.timestamp > timestamp:
			last = log_entry
	
	return last

def build_change_list(log:binhistory.BinLog, sequences:list[avb.trackgroups.Composition]) -> dict[binhistory.BinLogEntry, list[avb.trackgroups.Composition]]:
	"""Determine who changed what"""

	for sequence in sorted(sequences, key=lambda s: s.last_modified, reverse=True):
		log_entry= get_log_entry_for_timestamp(log, sequence.last_modified)
		if log_entry not in changes:
			changes[log_entry] = []
		changes[log_entry].append(sequence)
	
	return changes


if __name__ == "__main__":

	# Validate bin path
	if not len(sys.argv) > 1:
		print(USAGE, file=sys.stderr)
		sys.exit(2)

	path_bin = pathlib.Path(sys.argv[1])
	
	if not path_bin.is_file() or not path_bin.suffix.lower() == ".avb":
		print(f"Not a valid Avid bin (.avb): {sys.argv[1]}", file=sys.stderr)
		sys.exit(3)
	
	# Get the log
	try:
		log = binhistory.BinLog.from_bin(sys.argv[1])
	except binhistory.exceptions.BinLogNotFoundError:
		print("No `.log` file exists for this bin; nothing to do")
		sys.exit()
	except binhistory.exceptions.BinLogParseError as e:
		print(f"Error parsing log: {e}", file=sys.stderr)
	
	if not log:
		print("The `.log` file for this bin is empty; nothing to do")
		sys.exit()
	
	# Lock the bin and open it
	print(f"Reading bin {path_bin.name}...")
	try:
		with binlock.BinLock("zAutomation").hold_bin(path_bin), avb.open(path_bin) as avb_handle:
			sequences = list(avb_handle.content.toplevel())
	except binlock.exceptions.BinLockExistsError as e:
		print("The bin is currently locked.  Changes must not be made while reading", file=sys.stderr)
		sys.exit(4)

	if not sequences:
		print("No sequences found in bin; nothing to do")
		sys.exit()

	sorted_log = sorted(log, key=lambda l:l.timestamp, reverse=True)
	changes = build_change_list(sorted_log, sequences)

	for change in changes:
		print("")
		print(f"Modified by {change.computer} around {change.timestamp.strftime('%Y %B %d @ %I:%M %p')}")
		for sequence in changes[change]:
			print(f"\t{sequence.name}  {sequence.last_modified.strftime('%Y %B %d @ %I:%M %p')}")
	