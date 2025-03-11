import dataclasses, datetime, typing
from .defaults import DEFAULT_COMPUTER, DEFAULT_USER, FIELD_START_USER, FIELD_START_COMPUTER, DATETIME_STRING_FORMAT, MAX_FIELD_LENGTH
from .exceptions import BinLogParseError, BinLogInvalidFieldError, BinLogFieldLengthError

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

		# `user` should be a non-empty string of printable (not \n etc) characters
		if not isinstance(self.user, str):
			raise BinLogInvalidFieldError(f"`user` field must be a string (got {repr(self.user)})")
		elif not self.user.strip() or len(self.user) > MAX_FIELD_LENGTH:
			raise BinLogFieldLengthError(f"`user` field must be between 1 and {MAX_FIELD_LENGTH} characters long (got {len(self.user)})")
		elif not self.user.isprintable():
			raise BinLogInvalidFieldError(f"`user` field contains invalid characters")

		# `computer` should be a non-empty string of printable (not \n etc) characters
		if not isinstance(self.computer, str):
			raise BinLogInvalidFieldError(f"`computer` field must be a string (got {repr(self.computer)})")
		elif not self.computer.strip() or len(self.computer) > MAX_FIELD_LENGTH:
			raise BinLogFieldLengthError(f"`computer` field must be between 1 and {MAX_FIELD_LENGTH} characters long (got {len(self.computer)})")
		elif not self.computer.isprintable():
			raise BinLogInvalidFieldError(f"`computer` field contains invalid characters")
		
		# `timestamp` should be a `datetime.datetime`
		if not isinstance(self.timestamp, datetime.datetime):
			raise BinLogInvalidFieldError(f"`timestamp` field must be a valid `datetime.datetime` object (got {repr(self.timestamp)})")

	def copy_with(self, **fields):
		"""Creates a copy of this `BinLogEntry`, with optional changes to specified fields"""
		from dataclasses import replace
		return replace(self, **fields)
	
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
			parsed_timestamp = cls._datetime_from_log_timestamp(entry_datetime, max_year)
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
	def _datetime_from_log_timestamp(timestamp:str, max_year:typing.Optional[int]=None) -> datetime.datetime:
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