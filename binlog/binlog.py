import dataclasses, datetime
from . import BinLogParseError

@dataclasses.dataclass
class BinLogEntry:
	"""An entry in a bin log"""

	timestamp:datetime.datetime
	"""Timestamp of last access"""

	computer:str
	"""Hostname of the system which accessed the bin"""

	user:str
	"""Username which accessed the bin"""

	@classmethod
	def from_string(cls, log_entry:str):
		"""Return the log entry from a given log entry string"""

		# TODO: Logs don't specify year -- maybe use date modified on the .log to determine year?
		# TODO: Also will need to ensure day name matches month/day for the determined year... oof
		try:
			entry_datetime   = log_entry[0:19]
			parsed_timestamp = datetime.datetime.strptime(entry_datetime, "%a %b %d %H:%M:%S")
		except ValueError as e:
			raise BinLogParseError(f"Unexpected value encountered while parsing access time \"{entry_datetime}\": {e}") from e
		
		
		entry_computer = log_entry[21:47]
		if not entry_computer.startswith("Computer: "):
			raise BinLogParseError(f"Unexpected value encountered while parsing computer namme: \"{entry_computer}\"")
		parsed_computer = entry_computer[10:].rstrip()

		entry_user = log_entry[47:67]
		if not entry_user.startswith("User: "):
			raise BinLogParseError(f"Unexpected value encountered while parsing user namme: \"{entry_user}\"")
		parsed_user = entry_user[6:].rstrip()

		return cls(
			timestamp = parsed_timestamp,
			computer  = parsed_computer,
			user      = parsed_user
		)
	
class BinLog:
	"""An .avb access log"""

	def __init__(self, entries:list[BinLogEntry]|None=None):
		self._entries:list[BinLogEntry] = entries or []
	
	@property
	def entries(self) -> list[BinLogEntry]:
		"""Iterate over the log entries"""
		return self._entries[:]

	@classmethod
	def from_filepath(cls, log_path:str):

		entries = []

		with open (log_path, "r") as log_handle:
			for entry in log_handle:
				entries.append(BinLogEntry.from_string(entry))
		
		return cls(entries)