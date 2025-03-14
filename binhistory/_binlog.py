"""
`BinLog` class (a.k.a THE MEAT)
"""

import collections, datetime, typing

from ._binlogentry import BinLogEntry
from .defaults import MAX_ENTRIES, DEFAULT_FILE_EXTENSION
from .exceptions import BinLogTypeError, BinLogNotFoundError, BinNotFoundError, BinLogParseError

class BinLog(collections.UserList):
	"""An .avb access log"""

	def __init__(self, entries:typing.Optional[typing.Iterable[BinLogEntry]]=None):

		if entries is None:
			super().__init__()
			return

		try:
			entries = list(entries)
		except TypeError as e:
			raise BinLogTypeError(f"`BinLog` must be initialized with an iterable of `BinLogEntry`s, or `None` (got {type(entries).__name__})") from e

		for entry in entries:
			self._validate_item(entry)

		super().__init__(entries)
	
	# Validators
	@staticmethod
	def _validate_item(item:typing.Any):
		"""Validate an item is the proper type"""
		if not isinstance(item, BinLogEntry):
			raise BinLogTypeError(f"Entries must be of type `BinLogEntry` (got {type(item).__name__})")
	
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
		if not isinstance(other, self.__class__):
			raise BinLogTypeError(f"Can only add another {self.__class__.__name__} (got {type(other).__name__})")
		return super().__add__(other)
	
	def __iadd__(self, other):
		if not isinstance(other, self.__class__):
			raise BinLogTypeError(f"Can only add another {self.__class__.__name__} (got {type(other).__name__})")
		return super().__iadd__(other)
	
	def insert(self, i, item):
		self._validate_item(item)
		return super().insert(i, item)
	
	def append(self, item):
		self._validate_item(item)
		return super().append(item)
	
	def extend(self, other):
		try:
			for o in other:
				self._validate_item(o)
		except TypeError as e:
			raise BinLogTypeError(e) from e
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

		try:
			with open (log_path, "r") as log_handle:
				return cls.from_stream(log_handle, max_year=max_year)
		except FileNotFoundError as e:
			raise BinLogNotFoundError(f"A log file was not found at the given path {log_path}") from e
		except UnicodeDecodeError as e:
			raise BinLogParseError(f"Error decoding log: {e}") from e
	
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
		return min(self) if self else None

	def latest_entry(self) -> typing.Optional[BinLogEntry]:
		"""Get the last/latest/most recent entry from a bin log"""
		return max(self) if self else None
	
	def users(self) -> typing.List[str]:
		"""Get a list of unique users in the log"""
		return list(set(e.user for e in self))
	
	def computers(self) -> typing.List[str]:
		"""Get a list of unique computers in the log"""
		return list(set(e.computer for e in self))
	
	def timestamps(self) -> typing.List[datetime.datetime]:
		"""Get a list of unique timestamps in the log"""
		return list(set(e.timestamp for e in self))
	
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
