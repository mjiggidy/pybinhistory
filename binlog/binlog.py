import dataclasses, datetime, typing, getpass, socket
from . import BinLogParseError, BinLogFieldLengthError, BinLogInvalidFieldError
from . import MAX_ENTRIES, DEFAULT_FILE_EXTENSION

MAX_FIELD_LENGTH:int = 15
"""Max number of characters in User or Computer fields"""

DATETIME_STRING_FORMAT:str = "%a %b %d %H:%M:%S"
"""Datetime string format for bin log entry (Example: Wed Dec 15 09:47:51)"""

FIELD_START_USER:str       = "User: "
DEFAULT_USER:str           = getpass.getuser()[:MAX_FIELD_LENGTH] or "Unknown"

FIELD_START_COMPUTER:str   = "Computer: "
DEFAULT_COMPUTER:str       = socket.gethostname()[:MAX_FIELD_LENGTH] or "Unknown"

@dataclasses.dataclass(frozen=True)
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
		
		# TODO: Additional validation
		# (Need to figure out any invalid characters)

		if not self.user.strip() or len(self.user) > MAX_FIELD_LENGTH:
			raise BinLogFieldLengthError(f"`user` field must be between 1 and {MAX_FIELD_LENGTH} characters long (got {len(self.user)}")
		if not self.user.isprintable():
			raise BinLogInvalidFieldError(f"`user` field contains invalid characters")
		if not self.computer.strip() or len(self.computer) > MAX_FIELD_LENGTH:
			raise BinLogFieldLengthError(f"`computer` field must be between 1 and {MAX_FIELD_LENGTH} characters long (got {len(self.computer)}")
		if not self.computer.isprintable():
			raise BinLogInvalidFieldError(f"`computer` field contains invalid characters")

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
	def from_string(cls, log_entry:str, max_year:int=datetime.datetime.now().year) -> "BinLogEntry":
		"""Return the log entry from a given log entry string"""
		try:
			entry_datetime   = log_entry[0:19]
			parsed_timestamp = cls.datetime_from_log_timestamp(entry_datetime, max_year)
		except ValueError as e:
			raise BinLogParseError(f"Unexpected value encountered while parsing access time \"{entry_datetime}\" (Assuming a max year of {max_year}): {e}") from e
		
		# Computer name: Observed to be AT LEAST 15 characters.  Likely the max but need to check.
		entry_computer = log_entry[21:47]
		if not entry_computer.startswith(FIELD_START_COMPUTER):
			raise BinLogParseError(f"Unexpected value encountered while parsing computer namme: \"{entry_computer}\"")
		parsed_computer = entry_computer[10:].rstrip()

		# User name: Observed to be max 15 characters (to end of line)
		entry_user = log_entry[47:68]
		if not entry_user.startswith(FIELD_START_USER):
			raise BinLogParseError(f"Unexpected value encountered while parsing user namme: \"{entry_user}\"")
		parsed_user = entry_user[6:].rstrip()

		return cls(
			timestamp = parsed_timestamp,
			computer  = parsed_computer,
			user      = parsed_user
		)
	
	@staticmethod
	def datetime_from_log_timestamp(timestamp:str, max_year:int) -> datetime.datetime:
		"""Form a datetime from a given timestamp string"""
		# NOTE: This is because timestamps in the .log file don't indicate the year, but they DO
		# indicate the day of the week.  So, to get a useful `datetime` object out of this, "we"
		# need to determine which year the month/day occurs on the particular day of the week
		# using `max_year` as a starting point (likely a file modified date, or current year)

		# Make the initial datetime from known info
		initial_date = datetime.datetime.strptime(timestamp, DATETIME_STRING_FORMAT)

		# Also get the weekday from the timestamp string for comparison
		wkday = timestamp[:3]

		# Search backwards up to 11 years
		for year in range(max_year, max_year - 11, -1):
			test_date = initial_date.replace(year=year)
			if test_date.strftime("%a") == wkday:
				return test_date

		raise ValueError(f"Could not determine a valid year for which {initial_date.month}/{initial_date.day} occurs on a {wkday}")
	
class BinLog:
	"""An .avb access log"""

	def __init__(self, entries:list[BinLogEntry]|None=None):
		self._entries:list[BinLogEntry] = [e for e in entries] if entries else []
	
	@property
	def entries(self) -> list[BinLogEntry]:
		"""Iterate over the log entries"""
		# TODO: Triple check that bin log entries usually are sorted by date...
		#return self._entries
		return sorted(self._entries, key=lambda e: e.timestamp)[-MAX_ENTRIES:]
	
	def __iter__(self):
		yield from self.entries

	def to_string(self) -> str:
		"""Format as string"""
		return str().join(e.to_string() + "\n" for e in self.entries)


	# Readers
	@classmethod
	def from_path(cls, log_path:str, max_year:int|None=None) -> "BinLog":
		"""Load from an existing .log file"""
		# NOTE: Encountered mac_roman, need to deal with older encodings sometimes
		with open (log_path, "r") as log_handle:
			return cls.from_stream(log_handle, max_year=max_year)
	
	@classmethod
	def from_stream(cls, file_handle:typing.TextIO, max_year:int|None) -> "BinLog":
		"""Parse a log from an open file handle"""
		import os
		
		stat_info = os.fstat(file_handle.fileno())
		max_year = max_year or datetime.datetime.fromtimestamp(stat_info.st_mtime).year

		entries = []
		for entry in file_handle:
			entries.append(BinLogEntry.from_string(entry, max_year=max_year))
		
		return cls(entries)

	# Writers	
	def to_path(self, file_path:str):
		"""Write log to filepath"""
		with open(file_path, "w", encoding="utf-8") as output_handle:
			self.to_stream(output_handle)
	
	def to_stream(self, file_handle:typing.TextIO):
		"""Write log to given stream"""
		file_handle.write(self.to_string())

	# Convenience methods	
	def last_entry(self) -> BinLogEntry|None:
		"""Get the last/latest/most recent entry from a bin log"""
		return self.entries[-1] if self.entries else  None
	
	@classmethod
	def touch(cls, log_path:str, entry:typing.Optional[BinLogEntry]=None):
		"""Add an entry to a log file"""
		import pathlib

		entries = [entry or BinLogEntry()]

		# Read in any existing entries
		if pathlib.Path(log_path).is_file():
			entries.extend(cls.from_path(log_path).entries)
		
		BinLog(entries).to_path(log_path)
	
	@staticmethod
	def log_path_from_bin_path(bin_path:str) -> str:
		"""Determine the expected log path for a given bin path"""
		import pathlib
		return str(pathlib.Path(bin_path).with_suffix(DEFAULT_FILE_EXTENSION))
	
	def __repr__(self) -> str:
		last_entry = self.last_entry()
		last_entry_str = last_entry.to_string().rstrip() if last_entry else None
		return f"<{self.__class__.__name__} entries={len(self.entries)} last_entry={last_entry_str}>"
