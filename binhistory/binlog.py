"""
`BinLog` and `BinLogEntry` classes (a.k.a THE MEAT)
"""

import collections.abc
import dataclasses, datetime, typing, collections
from .exceptions import BinLogParseError, BinLogFieldLengthError, BinLogInvalidFieldError, BinLogTypeError, BinLogNotFoundError, BinNotFoundError
from .defaults import MAX_ENTRIES, DEFAULT_FILE_EXTENSION, DEFAULT_USER, DEFAULT_COMPUTER, MAX_FIELD_LENGTH, DATETIME_STRING_FORMAT, FIELD_START_COMPUTER, FIELD_START_USER

@dataclasses.dataclass(frozen=True, order=True)
class BinLogEntry:
	"""An entry in a bin log"""

	timestamp:datetime.datetime = dataclasses.field(default_factory=lambda: datetime.datetime.now())
	"""Timestamp of last access"""

	computer:str = DEFAULT_COMPUTER
	"""Hostname of the system which accessed the bin"""

	user:str = DEFAULT_USER
	"""User profile which accessed the bin"""

	def __post_init__(self):
		"""Validate fields"""

		if not isinstance(self.user, str):
			raise BinLogInvalidFieldError(f"`user` field must be a string (got {repr(self.user)})")
		elif not self.user.strip() or len(self.user) > MAX_FIELD_LENGTH:
			raise BinLogFieldLengthError(f"`user` field must be between 1 and {MAX_FIELD_LENGTH} characters long (got {len(self.user)})")
		elif not self.user.isprintable():
			raise BinLogInvalidFieldError(f"`user` field contains invalid characters")

		if not isinstance(self.computer, str):
			raise BinLogInvalidFieldError(f"`computer` field must be a string (got {repr(self.computer)})")
		elif not self.computer.strip() or len(self.computer) > MAX_FIELD_LENGTH:
			raise BinLogFieldLengthError(f"`computer` field must be between 1 and {MAX_FIELD_LENGTH} characters long (got {len(self.computer)})")
		elif not self.computer.isprintable():
			raise BinLogInvalidFieldError(f"`computer` field contains invalid characters")
		
		if not isinstance(self.timestamp, datetime.datetime):
			raise BinLogInvalidFieldError(f"`timestamp` field must be a valid `datetime.datetime` object (got {repr(self.timestamp)})")

	def to_string(self) -> str:
		"""Format the bin log entry as a string"""
		format_datetime       = self.timestamp.strftime(DATETIME_STRING_FORMAT)
		format_entry_computer = FIELD_START_COMPUTER + self.computer
		format_entry_user     = FIELD_START_USER + self.user

		return str().join([
			format_datetime.ljust(21),
			format_entry_computer.ljust(26),
			format_entry_user.ljust(21)
		])
	
	@classmethod
	def from_string(cls, log_entry:str, max_year:typing.Optional[int]=None) -> "BinLogEntry":
		"""Return the log entry from a given log entry string"""

		try:
			entry_datetime   = log_entry[0:19]
			parsed_timestamp = cls.datetime_from_log_timestamp(entry_datetime, max_year)
		except ValueError as e:
			raise BinLogParseError(f"Unexpected value encountered while parsing access time \"{entry_datetime}\" (Assuming a max year of {max_year}): {e}") from e
		
		# Computer name: Observed to be AT LEAST 15 characters.  Likely the max but need to check.
		entry_computer = log_entry[21:47]
		if not entry_computer.startswith(FIELD_START_COMPUTER):
			raise BinLogParseError(f"Unexpected value encountered while parsing computer name: \"{entry_computer}\"")
		parsed_computer = entry_computer[10:].rstrip()

		# User name: Observed to be max 15 characters (to end of line)
		entry_user = log_entry[47:68]
		if not entry_user.startswith(FIELD_START_USER):
			raise BinLogParseError(f"Unexpected value encountered while parsing user name: \"{entry_user}\"")
		parsed_user = entry_user[6:].rstrip()

		return cls(
			timestamp = parsed_timestamp,
			computer  = parsed_computer,
			user      = parsed_user
		)
	
	@staticmethod
	def datetime_from_log_timestamp(timestamp:str, max_year:typing.Optional[int]=None) -> datetime.datetime:
		"""
		Form a datetime from a given timestamp string
		
		This gets a little complicated  because timestamps in the .log file don't indicate the year, but they DO
		indicate the day of the week.  So, to get a useful :class:``datetime.datetime`` object out of this, "we" need to determine 
		which year the month/day occured on the particular day of the week using ``max_year`` as a starting point 
		(likely a file modified date, or current year), and counting backwards until we get a good match.

		Also accounting for Feb 29 leap year stuff.  It's been fun.
		"""
		
		import calendar

		if max_year is None:
			max_year = datetime.datetime.now().year

		# Account for leap year
		needs_leapyear = "Feb 29" in timestamp
		while needs_leapyear and not calendar.isleap(max_year):
			max_year -= 1

		# Make the initial datetime from known info
		# NOTE: Appending `max_year` here primarily to avoid invalid leap year timestamps
		initial_date = datetime.datetime.strptime(timestamp + " " + str(max_year), DATETIME_STRING_FORMAT + " %Y")

		# Also get the weekday from the timestamp string to compare against the parsed datetime.datetime weekday
		wkday = timestamp[:3]

		# Search backwards up to 11 years (when weekday/date pairs start repeating)
		for year in range(max_year, max_year - 11, -1):

			if needs_leapyear and not calendar.isleap(year):
				continue

			test_date = initial_date.replace(year=year)
			
			if test_date.strftime("%a") == wkday:
				return test_date

		raise ValueError(f"Could not determine a valid year for which {initial_date.month}/{initial_date.day} occurs on a {wkday}")

class BinLog(collections.UserList):
	"""An .avb access log"""

	def __init__(self, entries:typing.Optional[typing.Iterable[BinLogEntry]]=None):

		if entries is None:
			super().__init__()
			return

		try:
			entries = list(entries)
		except TypeError as e:
			raise BinLogTypeError(f"`BinLog` must be initialized with an iterable of `BinLogEntry`s, or `None` (got {repr(entries)})") from e

		for entry in entries:
			self._validate_item(entry)

		super().__init__(entries)
	
	# Validators
	@staticmethod
	def _validate_item(item:typing.Any):
		"""Validate an item is the proper type"""
		if not isinstance(item, BinLogEntry):
			raise BinLogTypeError(f"Entries must be of type `BinLogEntry` (got {repr(item)})")
	
	def __iter__(self) -> typing.Iterator[BinLogEntry]:
		# For typehints
		return super().__iter__()
	
	def __getitem__(self, key:int) -> BinLogEntry:
		# For typehints
		return super().__getitem__(key)
	
	def __setitem__(self, index:int, item:typing.Any):
		self._validate_item(item)
		super().__setitem__(index, item)
	
	def __add__(self, other):
		self._validate_item(other)
		return super().__add__(other)
	
	def __iadd__(self, other):
		self._validate_item(other)
		return super().__iadd__(other)
	
	def insert(self, i, item):
		self._validate_item(item)
		return super().insert(i, item)
	
	def append(self, item):
		self._validate_item(item)
		return super().append(item)
	
	def extend(self, other):
		self._validate_item(other)
		return super().extend(other)
	
	# Formatters
	def to_string(self) -> str:
		"""Format as string"""
		sorted_entries = sorted(self)[-MAX_ENTRIES:]
		return str().join(e.to_string() + "\n" for e in sorted_entries)

	# Readers
	@classmethod
	def from_bin(cls, bin_path:str, missing_bin_ok:bool=True, max_year:typing.Optional[int]=None) -> "BinLog":
		"""Load an existing .log file for a given bin"""
		return cls.from_path(BinLog.log_path_from_bin_path(bin_path, missing_bin_ok=missing_bin_ok), max_year)

	@classmethod
	def from_path(cls, log_path:str, max_year:typing.Optional[int]=None) -> "BinLog":
		"""Load from an existing .log file"""
		# NOTE: Encountered mac_roman, need to deal with older encodings sometimes

		import pathlib

		if not pathlib.Path(log_path).is_file():
			raise BinLogNotFoundError(f"A log file was not found at the given path {log_path}")

		with open (log_path, "r") as log_handle:
			return cls.from_stream(log_handle, max_year=max_year)
	
	@classmethod
	def from_stream(cls, file_handle:typing.TextIO, max_year:typing.Optional[int]=None) -> "BinLog":
		"""Parse a log from an open file handle"""
		import os
		
		# If we didn't get a `max_year` anywhere else, use the mtime
		if not max_year:
			stat_info = os.fstat(file_handle.fileno())
			max_year =datetime.datetime.fromtimestamp(stat_info.st_mtime).year

		entries = []
		for entry in file_handle:
			entries.append(BinLogEntry.from_string(entry, max_year=max_year))
		
		return cls(entries)

	# Writers
	def to_bin(self, bin_path:str, missing_bin_ok:bool=True):
		"""Write to a log for a given bin"""
		self.to_path(BinLog.log_path_from_bin_path(bin_path, missing_bin_ok=missing_bin_ok))

	def to_path(self, file_path:str):
		"""Write log to filepath"""
		with open(file_path, "w", encoding="utf-8") as output_handle:
			self.to_stream(output_handle)
	
	def to_stream(self, file_handle:typing.TextIO):
		"""Write log to given stream"""
		file_handle.write(self.to_string())

	# Convenience methods	
	def earliest_entry(self) -> typing.Optional[BinLogEntry]:
		"""Get the first/earliest entry from a bin log"""
		return sorted(self)[0] if self else None

	def latest_entry(self) -> typing.Optional[BinLogEntry]:
		"""Get the last/latest/most recent entry from a bin log"""
		return sorted(self)[-1] if self else None
	
	def users(self) -> typing.List[str]:
		"""Get a list of unique users in the log"""
		return list(set(e.user for e in self))
	
	def computers(self) -> typing.List[str]:
		"""Get a list of unique computers in the log"""
		return list(set(e.computer for e in self))
	
	@classmethod
	def touch(cls, log_path:str, entry:typing.Optional[BinLogEntry]=None):
		"""Add an entry to a log file"""
		import pathlib

		entries = [entry or BinLogEntry()]

		# Read in any existing entries
		if pathlib.Path(log_path).is_file():
			entries.extend(cls.from_path(log_path))
		
		BinLog(entries).to_path(log_path)
	
	@classmethod
	def touch_bin(cls, bin_path:str, entry:typing.Optional[BinLogEntry]=None, missing_bin_ok:bool=True):
		"""Add an entry to a log file for a given bin"""
		cls.touch(BinLog.log_path_from_bin_path(bin_path, missing_bin_ok), entry)
	
	@staticmethod
	def log_path_from_bin_path(bin_path:str, missing_bin_ok:bool=True) -> str:
		"""Determine the expected log path for a given bin path"""
		import pathlib
		if not missing_bin_ok and not pathlib.Path(bin_path).is_file():
			raise BinNotFoundError(f"An existing bin was not found at {bin_path}")
		return str(pathlib.Path(bin_path).with_suffix(DEFAULT_FILE_EXTENSION))
	
	def __repr__(self) -> str:
		last_entry = self.latest_entry()
		last_entry_str = last_entry.to_string().rstrip() if last_entry else None
		return f"<{self.__class__.__name__} entries={len(self)} last_entry={last_entry_str}>"
