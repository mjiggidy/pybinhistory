import pytest
import datetime
import os
import tempfile
from binhistory.binlog import BinLog, BinLogEntry
from binhistory.exceptions import (
    BinLogParseError, BinLogFieldLengthError, BinLogInvalidFieldError, BinLogTypeError, BinLogNotFoundError
)
from binhistory.defaults import DEFAULT_USER, DEFAULT_COMPUTER, MAX_FIELD_LENGTH, FIELD_START_COMPUTER, FIELD_START_USER

def test_binlog_entry_creation():
    entry = BinLogEntry()
    assert isinstance(entry.timestamp, datetime.datetime)
    assert entry.user == DEFAULT_USER
    assert entry.computer == DEFAULT_COMPUTER

def test_binlog_entry_validation():
    with pytest.raises(BinLogInvalidFieldError):
        BinLogEntry(user=123)  # Non-string user
    
    with pytest.raises(BinLogFieldLengthError):
        BinLogEntry(user=" " * (MAX_FIELD_LENGTH + 1))  # Exceeding length
    
    with pytest.raises(BinLogFieldLengthError):
        BinLogEntry(user="\n\t")  # Non-printable characters

def test_binlog_entry_to_string():
    entry = BinLogEntry(user="testuser", computer="testpc")
    entry_str = entry.to_string()
    assert "testuser" in entry_str
    assert "testpc" in entry_str

def test_binlog_entry_from_string_invalid():
    with pytest.raises(BinLogParseError):
        BinLogEntry.from_string("InvalidFormat")

def test_binlog_datetime_parsing():
    test_timestamp = "Mon Mar 04 12:34:56"
    parsed_date = BinLogEntry.datetime_from_log_timestamp(test_timestamp, max_year=2024)
    assert isinstance(parsed_date, datetime.datetime)
    assert parsed_date.year == 2024  # Ensures it picks the correct year

def test_binlog_datetime_parsing_invalid():
    with pytest.raises(ValueError):
        BinLogEntry.datetime_from_log_timestamp("InvalidTimestamp")

def test_binlog_operations():
    entries = [BinLogEntry(user=f"user{i}") for i in range(3)]
    log = BinLog(entries)
    
    assert len(log) == 3
    assert log.latest_entry().user == "user2"
    assert log.earliest_entry().user == "user0"
    
    log.append(BinLogEntry(user="newuser"))
    assert len(log) == 4

def test_binlog_empty():
    log = BinLog()
    assert len(log) == 0
    assert log.latest_entry() is None
    assert log.earliest_entry() is None

def test_binlog_file_operations():
    entries = [BinLogEntry(user=f"user{i}") for i in range(3)]
    log = BinLog(entries)
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        log.to_path(temp_file.name)
        
    loaded_log = BinLog.from_path(temp_file.name)
    assert len(loaded_log) == 3
    assert loaded_log.latest_entry().user == "user2"
    os.remove(temp_file.name)

def test_binlog_missing_file():
    with pytest.raises(BinLogNotFoundError):
        BinLog.from_path("/nonexistent/path.log")
