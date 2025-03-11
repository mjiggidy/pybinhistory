import unittest, datetime, pathlib
from binhistory import BinLog, BinLogEntry, exceptions, defaults

PATH_BIN = str(pathlib.Path(__file__).with_name("example.avb"))
PATH_LOG = str(pathlib.Path(__file__).with_name("example.log"))

class TestBinLog(unittest.TestCase):

	def test_defaults(self):

		default_log = BinLog()
		self.assertFalse(default_log)
		self.assertCountEqual(default_log, [])
	
	def test_create(self):

		with self.assertRaises(exceptions.BinLogTypeError):
			BinLog(BinLogEntry())
		
		with self.assertRaises(exceptions.BinLogTypeError):
			BinLog("peepee")
		
		with self.assertRaises(exceptions.BinLogTypeError):
			BinLog([BinLog(), "uh oh stinky"])
		
		logs = [BinLogEntry() for _ in range(20)] # So BinLogEntry()s have different timestamps
		self.assertCountEqual(BinLog(logs), logs)
		self.assertCountEqual(BinLog(l for l in logs), logs)
		self.assertEqual(len(BinLog(logs)), len(logs))

	def test_from_bin(self):

		self.assertEqual(BinLog.log_path_from_bin_path(PATH_BIN), PATH_LOG)

		log_raw    = pathlib.Path(PATH_LOG).read_text(encoding="utf-8")
		log_parsed = BinLog.from_bin(PATH_BIN)
		self.assertEqual(log_parsed.to_string(), log_raw)

		log_parsed.append(log_parsed.earliest_entry().copy_with(computer="Heehee"))
		self.assertEqual(log_parsed.to_string(), log_raw)




if __name__ == "__main__":

	unittest.main()