import sys
from binlog import BinLog

good = 0
bad = 0
skip = 0

# Use `-l examples.txt` to feed a text (`examples.txt`) file full of paths to .log files
# Or just give 'er a list of .logs directly as arguments
# Quick n dirty, I know
if "-l" in sys.argv:
	with open(sys.argv[sys.argv.index("-l") + 1]) as handle:
		log_list = [l.rstrip() for l in handle.readlines()]
else:
	log_list = sys.argv[1:]


for path_log in log_list:
	
	try:
		log = BinLog.from_filepath(path_log)
	except Exception as e:
		print(f"[Skipping {path_log}]: {e}")
		skip += 1
		continue


	with open(path_log, errors="replace") as handle:
		orig = handle.read()

	if log.to_string() != orig:
		
		print(path_log)

		for entry in log.entries:
			print(entry.to_string() + "   " + str(entry.timestamp.year))
		
		print()
		print(orig)
		print()
		print(log.to_string() == orig)

		bad += 1
	
	else:
		good += 1

print(f"Good: {good},   Bad: {bad}   Skip: {skip}")
	