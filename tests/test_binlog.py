import unittest, tempfile, pathlib, time, datetime
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
	
	def test_from_bin_missing(self):

		with self.assertRaises(exceptions.BinNotFoundError):
			BinLog.from_bin("example2.avb", missing_bin_ok=False)
		
		with self.assertRaises(exceptions.BinLogNotFoundError):
			BinLog.from_bin("example2.avb", missing_bin_ok=True)

	def test_list_operations(self):

		log = BinLog.from_path(PATH_LOG)
		
		# Check types
		with self.assertRaises(exceptions.BinLogTypeError):
			log.append([BinLogEntry()])
		with self.assertRaises(exceptions.BinLogTypeError):
			log.extend(BinLogEntry())
		with self.assertRaises(exceptions.BinLogTypeError):
			log + BinLogEntry()
		with self.assertRaises(exceptions.BinLogTypeError):
			log[4] = "No"
		
		# Basics
		log.append(BinLogEntry())
		log.extend([BinLogEntry(), BinLogEntry()])
		del log[3]

		# Add logs
		self.assertEqual(len(log), 12)
		log += log
		self.assertEqual(len(log), 12*2)

		# Contains
		entry = BinLogEntry()
		log[4] = entry
		self.assertTrue(entry in log)
		self.assertEqual(log.count(entry), 1)
	
	def test_stats(self):

		log = BinLog.from_path(PATH_LOG)
	
		# Raw strings
		with open(PATH_LOG) as handle_log:
			raw_log = handle_log.read()
		earliest_string = raw_log.split("\n")[0]
		latest_string   = raw_log.split("\n")[-2]	# Very last line is empty

		self.assertEqual(log.earliest_entry().to_string(), earliest_string)
		self.assertEqual(log.latest_entry().to_string(), latest_string)

		# Hacky but DYNAMIC
		user_count = 0
		computer_count = 0
		for user in log.users():
			user_count += raw_log.count(user)
		for computer in log.computers():
			computer_count += raw_log.count(computer)
		
		self.assertEqual(len(log), 10)
		self.assertEqual(user_count, 10)
		self.assertEqual(computer_count, 10)
		self.assertEqual(len(log.timestamps()), 10)
	
	def test_writes(self):

		# From Existing
		existing_log = BinLog.from_path(PATH_LOG)

		with tempfile.TemporaryDirectory() as temp_dir:
			temp_dir = pathlib.Path(temp_dir)

			existing_log.to_path(temp_dir/"from_existing.log")
		
			# Overwite
			existing_log.to_path(temp_dir/"from_existing.log")

			# For bin
			existing_log.to_bin(temp_dir/"poopoo.avb")
			self.assertEqual(BinLog.from_path(temp_dir/"poopoo.log").to_string(), existing_log.to_string())

			# Fail non-existing bin
			with self.assertRaises(exceptions.BinNotFoundError):
				existing_log.to_bin(temp_dir/"poopoo.avb", missing_bin_ok=False)
	
			# Test MAX_ENTRIES by adding an additional and making sure they're rotated properly
			max_log = BinLog.from_path(PATH_LOG)
			curr_timestamp = datetime.datetime.now().replace(microsecond=0)
			max_log.append(BinLogEntry(timestamp=curr_timestamp))			
			self.assertEqual(len(max_log), defaults.MAX_ENTRIES+1)
			max_log.to_path(temp_dir/"overflow.log")

			max_log_check = BinLog.from_path(temp_dir/"overflow.log")
			self.assertEqual(len(max_log_check), defaults.MAX_ENTRIES)
			self.assertEqual(max_log_check.latest_entry().timestamp, curr_timestamp)
			self.assertEqual(max_log_check.earliest_entry().timestamp, max_log[1].timestamp)
	
	def test_touch(self):

		hostname = defaults.DEFAULT_COMPUTER
		username = defaults.DEFAULT_USER

		with tempfile.TemporaryDirectory() as temp_dir:
			temp_dir = pathlib.Path(temp_dir)

			with self.assertRaises(exceptions.BinNotFoundError):
				BinLog.touch_bin(temp_dir/"weewee.avb", missing_bin_ok=False)

			# Allow no bin
			BinLog.touch_bin(temp_dir/"peepee.avb")

			that_new_log = BinLog.from_path(temp_dir/"peepee.log")

			self.assertEqual(len(that_new_log), 1)
			self.assertEqual(that_new_log[0].user, username)
			self.assertEqual(that_new_log[0].computer, hostname)

			first_timestamp = that_new_log[0].timestamp

			time.sleep(1)

			# Touch it again
			BinLog.touch_bin(temp_dir/"peepee.avb")
			that_new_log = BinLog.from_path(temp_dir/"peepee.log")

			self.assertEqual(len(that_new_log), 2)
			self.assertEqual(that_new_log[1].user, username)
			self.assertEqual(that_new_log[1].computer, hostname)

			self.assertEqual(that_new_log[0].timestamp, first_timestamp)
			self.assertNotEqual(that_new_log[0], that_new_log[1])

if __name__ == "__main__":

	unittest.main()