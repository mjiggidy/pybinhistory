# pybinhistory

*Because `pybinlog` was taken™*

`binhistory` is a python library for programmatically reading and writing Avid bin history log (`.log`) files in 
multi-user Avid Media Composer projects.

>[!WARNING]
> `binlog` is an unofficial library created for educational purposes.  While the ``.log`` file format
>is a very simple one, it is officially undocumented. Use this library at your own risk -- the developer assumes
>no responsibility for any damage to your project, loss of data, or weird snippy drama about who threw the audio
>out of sync in the latest version of the reel.

## Interesting Uses

- Be a good citizen!  Add a bin log entry when modifying a bin programmatically via automation/pipeline-y operations.
- Snoop around!  Easily gather metrics about modifications made by particular machines or users.
- Makes you look cool!  Everyone will be very impressed with you.  "Wow!" they'll say.

## Installation

Install the `pybinhistory` package [from PyPI](https://pypi.org/project/pybinhistory/) using `pip`:

```bash
pip install pybinhistory
```

Or clone from this repo:

```bash
git clone https://github.com/mjiggidy/pybinhistory.git
cd pybinhistory
pip install .
```

Now you can import `binhistory`!

```python
from binhistory import BinLog, BinLogEntry

# Write a log entry
BinLog.touch_bin("Reel 1.avb")

# See that last entry
log = BinLog.from_bin("Reel 1.avb").latest_entry()
print(f"Latest log entry was from {log.computer} at {log.timestamp}")
```

## Usage

See [readthedocs.io](https://pybinhistory.readthedocs.io) for general usage and API documentation!

## See Also
- [`pybinlock`](https://github.com/mjiggidy/pybinlock) - Programmatically read and write Avid bin lock (`.lck`) files
