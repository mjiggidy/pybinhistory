import unittest, datetime
from binhistory import BinLogEntry, exceptions, defaults

EXAMPLE_STRING = "Mon Mar 10 17:32:54  Computer: zMichael        User: poop           "
EXAMPLE_DATE   = datetime.datetime(year=2025, month=3, day=10, hour=17, minute=32, second=54)
EXAMPLE_ENTRY  = BinLogEntry(timestamp=EXAMPLE_DATE, computer="zMichael", user="poop")

class TestBinLogEntry(unittest.TestCase):

	def test_defaults(self):

		timestamp = datetime.datetime.now()
		self.assertEqual(
			BinLogEntry(timestamp=timestamp),
			BinLogEntry(timestamp=timestamp, user=defaults.DEFAULT_USER, computer=defaults.DEFAULT_COMPUTER)
		)

	def test_parse_string_date(self):

		log_entry = BinLogEntry.from_string(EXAMPLE_STRING, max_year=2025)

		self.assertEqual(log_entry.computer, "zMichael")
		self.assertEqual(log_entry.user, "poop")
		self.assertEqual(log_entry.timestamp, datetime.datetime(year=2025, month=3, day=10, hour=17, minute=32, second=54))

		with self.assertRaises(exceptions.BinLogParseError):
			BinLogEntry.from_string("Mon Mar 10 17:32:54  Computer:zMichael        User: poop           ")
		with self.assertRaises(exceptions.BinLogParseError):
			BinLogEntry.from_string("Mon Mar 32 17:32:54  Computer: zMichael        User: poop           ")
		
		# Leap year nonsense
		leaplog = BinLogEntry.from_string("Mon Feb 29 17:32:54  Computer: zMichael        User: poop           ", max_year=2025)
		self.assertEqual(leaplog.timestamp.year, 2016)
		
		with self.assertRaises(exceptions.BinLogParseError):
			BinLogEntry.from_string("Tue Feb 29 17:32:54  Computer: zMichael        User: poop           ", max_year=2025)
		

	def test_to_string(self):

		self.assertEqual(EXAMPLE_ENTRY.to_string(), EXAMPLE_STRING)

	def test_from_string_validation(self):

		with self.assertRaises(exceptions.BinLogInvalidFieldError):
			BinLogEntry(timestamp=None)
		with self.assertRaises(exceptions.BinLogInvalidFieldError):
			BinLogEntry(timestamp="Today")

		# Computer
		with self.assertRaises(exceptions.BinLogFieldLengthError):
			BinLogEntry(computer="")
		with self.assertRaises(exceptions.BinLogFieldLengthError):
			BinLogEntry(computer="ReallyBigOldName")
		with self.assertRaises(exceptions.BinLogInvalidFieldError):
			BinLogEntry(computer="My\nGoodness")

		# User
		with self.assertRaises(exceptions.BinLogFieldLengthError):
			BinLogEntry(user="")
		with self.assertRaises(exceptions.BinLogFieldLengthError):
			BinLogEntry(user="ReallyBigOldName")
		with self.assertRaises(exceptions.BinLogInvalidFieldError):
			BinLogEntry(user="My\nGoodness")
	
	def test_copy(self):
		
		self.assertEqual(
			EXAMPLE_ENTRY.copy_with(user="peepee"),
			BinLogEntry(timestamp=EXAMPLE_ENTRY.timestamp, user="peepee", computer=EXAMPLE_ENTRY.computer)
		)

		with self.assertRaises(exceptions.BinLogInvalidFieldError):
			EXAMPLE_ENTRY.copy_with(user="pee\tpee")
	
	def test_sort(self):

		# Cuz those timestamps be different
		self.assertLess(BinLogEntry(), BinLogEntry())
		self.assertNotEqual(BinLogEntry(), BinLogEntry())
		self.assertFalse(BinLogEntry() > BinLogEntry())

if __name__ == "__main__":

	unittest.main()