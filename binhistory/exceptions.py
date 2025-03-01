"""
Bespoke ``Exception``\s raised by ``pybinhistory``
"""

class BinLogParseError(ValueError):
	"""An invalid value was encountered while parsing the log"""

class BinLogFieldLengthError(ValueError):
	"""A log field is not a valid length (between 1 and ``MAX_FIELD_LENGTH`` chars)"""

class BinLogInvalidFieldError(ValueError):
	"""A log field contains invalid data"""

class BinLogTypeError(TypeError):
	"""A log entry is not a valid type"""