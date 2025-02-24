"""
Given a path to an Avid project directory, print some interesting stats 
about the log files within.  Okay well I think it's pretty neat.
"""

from binlog import BinLog, BinLogEntry
import sys, pathlib

USAGE = f"{pathlib.Path(__file__)} avid_project_dir"

# Stats
logs_good = 0
"""Logs succesfully read"""
logs_bad  = 0
"""Logs that weren't kind"""

user_counts:dict[str,int] = dict()
"""Number of entries per user"""
computer_counts:dict[str,int] = dict()
"""Number of entries per computer"""

oldest_log:BinLogEntry = None
"""Earliest log entry"""
oldest_log_path:str = None
"""Log path containing the earliest log entry"""

newest_log:BinLogEntry = None
"""Latest log entry"""
newest_log_path = None
"""Log path contining the latest log entry"""



if __name__ == "__main__":

	if not len(sys.argv) > 1:
		print(USAGE, file=sys.stderr)
		sys.exit(1)
	
	if not pathlib.Path(sys.argv[1]).is_dir():
		print(f"{sys.argv[1]} is not a valid directory")
		print(USAGE)
		sys.exit(2)

# Loop through all known logs
for log_path in pathlib.Path(sys.argv[1]).rglob("*.log"):

	# Skip resource forks
	if log_path.name.startswith("."):
		continue

	# Read and print the log
	try:
		log = BinLog.from_path(log_path)
		print(f"{log_path}: {log}")
		logs_good += 1

	except Exception as e:
		print(f"{log_path}: {e}", file=sys.stderr)
		logs_bad += 1
		continue

	# Gather stats	
	entries = log.entries
	for entry in entries:

		# Count user
		if entry.user not in user_counts:
			user_counts[entry.user] = 0
		user_counts[entry.user] += 1

		# Count hostname
		if entry.computer not in computer_counts:
			computer_counts[entry.computer] = 0
		computer_counts[entry.computer] += 1

		# Get timestamp extremes
		if not entries:
			continue

		if not oldest_log or entries[0].timestamp < oldest_log.timestamp:
			oldest_log = entries[0]
			oldest_log_path = log_path

		if not newest_log or entries[-1].timestamp > newest_log.timestamp:
			newest_log = entries[-1]
			newest_log_path = log_path


print("")
print(f"{logs_good} log(s) valid;  {logs_bad} log(s) invalid")
print("")

if not logs_good:
	sys.exit(0)

# Print me them stats

print(f"{len(user_counts)} User Profile(s):")
for user,count in user_counts.items():
	print(f"{user.rjust()}  ({count} entries)")

print("")

print(f"{len(computer_counts)} System(s):")
for computer,count in computer_counts.items():
	print(f"{computer.rjust(15)}  ({count} entries)")

print("")

if oldest_log:
	print(f"Earliest log:  {oldest_log.timestamp.strftime(r'%Y %m %d @ %H:%M:%S')}")
	print(f"   From file:  {oldest_log_path}")
	print(f"  From entry:  {oldest_log.to_string()}")

print("")

if newest_log:
	print(f"  Latest log:  {newest_log.timestamp.strftime(r'%Y %m %d @ %H:%M:%S')}")
	print(f"   From file:  {newest_log_path}")
	print(f"  From entry:  {newest_log.to_string()}")

print("")