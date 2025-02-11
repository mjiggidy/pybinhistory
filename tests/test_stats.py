from binlog import BinLog, BinLogEntry
import sys, dataclasses, datetime

@dataclasses.dataclass
class LogStats:
	"""Lil stat struct fer yas"""
	date_earliest:datetime.datetime|None
	date_latest:datetime.datetime|None
	user_shortest:str|None
	user_longest:str|None
	computer_shortest:str|None
	computer_longest:str|None

def gather_stats(log:BinLog):

	entries = log.entries

	by_date = sorted(entries, key=lambda e: e.timestamp)
	by_user_length = sorted(entries, key=lambda e: len(e.user))
	by_computer_length = sorted(entries, key=lambda e: len(e.computer))

	return LogStats(
		date_earliest     = by_date[0].timestamp,
		date_latest       = by_date[-1].timestamp,
		user_shortest     = by_user_length[0].user,
		user_longest      = by_user_length[-1].user,
		computer_shortest = by_computer_length[0].computer,
		computer_longest  = by_computer_length[-1].computer
	)
		

# Use `-l examples.txt` to feed a text (`examples.txt`) file full of paths to .log files
# Or just give 'er a list of .logs directly as arguments\
# # Quick n dirty, I know
if "-l" in sys.argv:
	with open(sys.argv[sys.argv.index("-l") + 1]) as handle:
		log_list = [l.rstrip() for l in handle.readlines()]
else:
	log_list = sys.argv[1:]

master_stats = LogStats(
	None,None,None,None,None,None
)

counter = 0

for path_file in log_list:

	try:
		log = BinLog.from_filepath(path_file)
	except Exception as e:
		print(f"[Skipping {path_file}]: {e}")
		continue
	
	if not len(log.entries):
		print(f"[Skipping {path_file}]: No entries / empty log")
		continue
	
	log_stats = gather_stats(log)

	if master_stats.date_earliest is None or master_stats.date_earliest > log_stats.date_earliest:
		master_stats.date_earliest = log_stats.date_earliest

	if master_stats.date_latest is None or master_stats.date_latest < log_stats.date_latest:
		master_stats.date_latest = log_stats.date_latest

	if master_stats.user_shortest is None or len(master_stats.user_shortest) > len(log_stats.user_shortest):
		master_stats.user_shortest = log_stats.user_shortest

	if master_stats.user_longest is None or len(master_stats.user_longest) < len(log_stats.user_longest):
		master_stats.user_longest = log_stats.user_longest

	if master_stats.computer_shortest is None or len(master_stats.computer_shortest) > len(log_stats.computer_shortest):
		master_stats.computer_shortest = log_stats.computer_shortest

	if master_stats.computer_longest is None or len(master_stats.computer_longest) < len(log_stats.computer_longest):
		master_stats.computer_longest = log_stats.computer_longest

	counter += 1

if counter == 0:
	print("No logs applicable.")
	sys.exit()

print(f"From {counter} log entries:")
print(f"     Shortest Name:  {master_stats.user_shortest} ({len(master_stats.user_shortest)} chars)")
print(f"      Longest Name:  {master_stats.user_longest} ({len(master_stats.user_longest)} chars)")
print(f" Shortest Computer:  {master_stats.computer_shortest} ({len(master_stats.computer_shortest)} chars)")
print(f"  Longest Computer:  {master_stats.computer_longest} ({len(master_stats.computer_longest)} chars)")
print(f"     Earliest Date:  {master_stats.date_earliest}")
print(f"       Latest Date:  {master_stats.date_latest}")
