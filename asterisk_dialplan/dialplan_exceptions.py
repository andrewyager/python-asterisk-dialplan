""" Exception classes for asterisk_dialplan """

class DialplanException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)