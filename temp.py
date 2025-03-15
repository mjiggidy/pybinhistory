from binhistory import BinLog, BinLogEntry

# Write a log entry
BinLog.touch_bin("Reel 1.avb")

# See that last entry
log = BinLog.from_bin("Reel 1.avb").latest_entry()
print(f"Latest log entry was from {log.computer} at {log.timestamp}")