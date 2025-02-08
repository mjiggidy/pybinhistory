import sys
from binlog import BinLog

good = 0
bad = 0

for path_log in sys.argv[1:]:
	
	log = BinLog.from_filepath(path_log)

	with open(path_log) as handle:
		orig = handle.read()

	if log.to_string() != orig:
		
		print(path_log)

		print(log.to_string())
		print()
		print(orig)
		print()
		print(log.to_string() == orig)

		bad += 1
	
	else:
		good += 1

print(f"Good: {good},   Bad: {bad}")
	