from binlog import BinLog
import sys

print(BinLog.last_entry(sys.argv[1]))

