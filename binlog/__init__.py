MAX_ENTRIES:int = 10
"""Maximum log entries allowed in a file"""

DEFAULT_FILE_EXTENSION = ".log"
"""The expected file extension for bin log files"""

from .exceptions import BinLogParseError
from .binlog import BinLog, BinLogEntry