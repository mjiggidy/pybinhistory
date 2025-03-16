"""
:mod:`binhistory` is for reading and writing Avid bin ``.log`` files.

Written by Michael Jordan <michael@glowingpixel.com>
"""

from . import exceptions, defaults
from ._binlog import BinLog
from ._binlogentry import BinLogEntry