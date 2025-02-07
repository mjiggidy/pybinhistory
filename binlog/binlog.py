import dataclasses, datetime

class BinLogParseError(ValueError):
	"""An invalid value was encountered while parsing the log"""

class BinLog:
	"""An .avb access log"""

	def __init__(self):
		self._entries = []
	
	@property
	def entries(self):
		"""Iterate over the log entries"""
		yield self._entries
	
@dataclasses.dataclass
class BinLogEntry:
	timestamp:datetime.datetime
	"""Timestamp of last access"""

	computer:str
	"""Hostname of the system which accessed the bin"""

	user:str
	"""Username which accessed the bin"""

	@classmethod
	def from_string(cls, log_entry:str):
		"""Return the log entry from a given log entry string"""

		try:
			entry_datetime   = log_entry[0:20]
			parsed_timestamp = datetime.datetime.strptime(entry_datetime, "%a %b %d %H:%M:S")
		except ValueError as e:
			raise BinLogParseError(f"Unexpected value encountered while parsing access time \"{entry_datetime}\": {e}") from e
		
		
		entry_computer = log_entry[22:48]
		if not entry_computer.startswith("Computer: "):
			raise BinLogParseError(f"Unexpected value encountered while parsing computer namme: \"{entry_computer}\"")
		parsed_computer = entry_computer[10:].rstrip()

		entry_user = log_entry[48:69]
		if not entry_user.startswith("User: "):
			raise BinLogParseError(f"Unexpected value encountered while parsing user namme: \"{entry_user}\"")
		parsed_user = entry_user[6:].rstrip()

		return cls(
			timestamp = parsed_timestamp,
			computer  = parsed_computer,
			user      = parsed_user
		)