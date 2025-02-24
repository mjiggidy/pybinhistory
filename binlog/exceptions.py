class BinLogParseError(ValueError):
	"""An invalid value was encountered while parsing the log"""

class BinLogFieldLengthError(ValueError):
	"""A log field is not a valid length (between 1 and MAX_FIELD_LENGTH chars)"""

class BinLogInvalidFieldError(ValueError):
	"""A log field contains invalid data"""