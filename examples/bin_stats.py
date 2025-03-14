"""
Given an Avid project folder path, get last modified info for Avid bins
"""

import sys, pathlib
from binhistory import BinLog, exceptions

if __name__ == "__main__":

	if not len(sys.argv) > 1 or not pathlib.Path(sys.argv[1]).is_dir():
		print(f"Usage: {pathlib.Path(__file__)} avid_project_dir", file=sys.stderr)
		sys.exit(1)
	
	for path_bin in pathlib.Path(sys.argv[1]).rglob("*.avb"):

		# Skip dotfiles
		if path_bin.name.startswith("."):
			continue

		try:
			log = BinLog.from_bin(path_bin)
		except exceptions.BinLogNotFoundError:
			# Skip bins without logs
			continue
		except exceptions.BinLogParseError:
			# Silently skip bad logs
			continue
		if not log:
			# Skip empty logs
			continue

		last = log.latest_entry()

		print(f"{path_bin.name:>72}  :  Last modified by {last.computer} on {last.timestamp}")
		