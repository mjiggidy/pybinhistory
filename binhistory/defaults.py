"""
Sane defaults for internal use
"""

def _get_default_user() -> str:
	import getpass
	try:
		return getpass.getuser() or "pybinhistory"
	except:
		return "pybinhistory"

def _get_default_computer() -> str:
	import socket
	try:
		return socket.gethostname() or "pybinhistory"
	except:
		return "pybinhistory"

DEFAULT_FILE_EXTENSION:str = ".log"
"""The expected file extension for bin log files"""

MAX_ENTRIES:int = 10
"""Maximum log entries allowed in a file"""

MAX_FIELD_LENGTH:int = 15
"""Max number of characters in User or Computer fields"""
# NerdNote: I feel like this comes from NetBIOS max length of 15?

DATETIME_STRING_FORMAT:str = "%a %b %d %H:%M:%S"
"""Datetime string format for bin log entry (Example: Wed Dec 15 09:47:51)"""

FIELD_START_USER:str       = "User: "
DEFAULT_USER:str           = _get_default_user()[:MAX_FIELD_LENGTH]

FIELD_START_COMPUTER:str   = "Computer: "
DEFAULT_COMPUTER:str       = _get_default_computer()[:MAX_FIELD_LENGTH]