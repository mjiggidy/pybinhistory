from binlog import BinLog
import sys

BinLog.touch(sys.argv[1], "avidmac", "aviduser")