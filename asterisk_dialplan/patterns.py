from util import common_start

def build_safe_pattern(first_number, last_number):
	""" Builds a pattern that covers digits from first_number to last_number
	Assumes that this range is safe to generate a pattern for

	Will generate a DialplanException if first_number and last_number are not of equal length

	:param first_number: telephone number in E164 format
	:type first_number: integer
	:param last_number: telephoen number in E164 format
	:type last_number: integer
	:returns: string representing the pattern
	:rtype: string
	"""

	from dialplan_exceptions import DialplanException

	fn_string = str(first_number)
	ln_string = str(last_number)

	if len(fn_string) != len(ln_string):
		#the pattern to match is not valid
		raise DialplanException("First and last numbers are not of equal length")

	if int(first_number) > int(last_number):
		raise DialplanException("Last number is smaller than the first number")

	if first_number == last_number:
		return fn_string


	#lets work out the number of significant digits
	pattern = common_start(first_number,last_number)
	digit_start = int(len(pattern))
	digits = len(str(first_number)) - len(pattern)
	strip_digits = int(digits*-1)
	remaining_fn = fn_string[strip_digits:]
	remaining_ln = ln_string[strip_digits:]

	for fdigit, ldigit in zip(list(remaining_fn),list(remaining_ln)):
		if fdigit == "0" and ldigit == "9":
			pattern = pattern + "X"
		elif fdigit == "1" and ldigit == "9":
			pattern = pattern + "Z"
		elif fdigit == "2" and ldigit == "9":
			pattern = pattern + "N"
		else:
			pattern = pattern + "[" + fdigit + "-" + ldigit + "]"

	return "_"+pattern

def generate_patterns(low,high):
	""" Builds a list of patterns that cover the E.164 numbers between low and high 

	Will generate a DialplanException if first_number and last_number are not of equal length

	:param first_number: telephone number in E164 format
	:type first_number: integer
	:param last_number: telephoen number in E164 format
	:type last_number: integer
	:returns: list of strings representing the pattern
	:rtype: list

	"""

	from ranges import split_range

	from dialplan_exceptions import DialplanException

	#get the string and integer reps of the numbers
	fn_string = str(low)
	ln_string = str(high)

	low = int(low)
	high = int(high)

	if len(fn_string) != len(ln_string):
		#the pattern to match is not valid
		raise DialplanException("First and last numbers are not of equal length")

	if low > high:
		raise DialplanException("Last number is smaller than the first number")

	patterns = []

	range_list = split_range(low,high)
	for rangeTuple in range_list:
		patterns.append(build_safe_pattern(rangeTuple[0], rangeTuple[1]))
	return patterns
