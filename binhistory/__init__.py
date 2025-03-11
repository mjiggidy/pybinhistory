"""
:mod:`binhistory` is for working with Avid bin ``.log`` files.

It is designed to help developers read and write valid bin logs 
without a whole lotta fuss.

Tenderly over-engineered by Michael Jordan <michael@glowingpixel.com> while he struggled to find his next AE gig.
"""

from . import exceptions, defaults
from ._binlog import BinLog
from ._binlogentry import BinLogEntry