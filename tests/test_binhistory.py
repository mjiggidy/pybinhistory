import pytest
import datetime
from binhistory.binlog import BinLogEntry, BinLog
from binhistory.exceptions import BinLogParseError, BinLogFieldLengthError, BinLogInvalidFieldError, BinLogTypeError
from binhistory.defaults import MAX_FIELD_LENGTH

# Test BinLogEntry creation and validation
def test_binlog_entry_valid():
	entry = BinLogEntry(timestamp=datetime.datetime(2024, 2, 26, 10, 30), computer="MyPC", user="Alice")
	assert entry.timestamp.year == 2024
	assert entry.computer == "MyPC"
	assert entry.user == "Alice"

def test_binlog_entry_invalid_length():
	with pytest.raises(BinLogFieldLengthError):
		BinLogEntry(computer="X" * (MAX_FIELD_LENGTH + 1), user="Alice")
	with pytest.raises(BinLogFieldLengthError):
		BinLogEntry(computer="MyPC", user="")

def test_binlog_entry_invalid_characters():
	with pytest.raises(BinLogInvalidFieldError):
		BinLogEntry(computer="Invalid\nName", user="Alice")

def test_binlog_entry_to_string():
	entry = BinLogEntry(timestamp=datetime.datetime(2024, 2, 26, 10, 30), computer="MyPC", user="Alice")
	formatted = entry.to_string()
	assert "MyPC" in formatted
	assert "Alice" in formatted

def test_binlog_entry_from_string():
	log_string = "Wed Feb 26 10:30:00  Computer: MyPC            User: Alice       "
	entry = BinLogEntry.from_string(log_string)
	assert entry.computer == "MyPC"
	assert entry.user == "Alice"

def test_binlog_entry_invalid_parse():
	with pytest.raises(BinLogParseError):
		BinLogEntry.from_string("Invalid log entry")

# Test BinLog class
def test_binlog_empty():
	log = BinLog()
	assert len(log.entries) == 0

def test_binlog_add_entries():
	entry = BinLogEntry(computer="MyPC", user="Alice")
	log = BinLog([entry])
	assert len(log.entries) == 1
	assert log.entries[0].computer == "MyPC"

def test_binlog_invalid_entry():
	with pytest.raises(BinLogTypeError):
		BinLog(["InvalidEntry"])

def test_binlog_last_entry():
	entry1 = BinLogEntry(timestamp=datetime.datetime(2024, 2, 26, 10, 0), computer="PC1", user="Bob")
	entry2 = BinLogEntry(timestamp=datetime.datetime(2024, 2, 26, 11, 0), computer="PC2", user="Alice")
	log = BinLog([entry1, entry2])
	assert log.last_entry().computer == "PC2"
