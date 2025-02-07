import sys
from binlog import BinLog

log = BinLog.from_filepath(sys.argv[1])

for entry in log.entries:
	print(entry)