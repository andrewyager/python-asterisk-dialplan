from util import common_start
import math

def split_range(low, high):
	""" Take a range of telephone numbers in E.164 format between low and high and return
	the "safe" chunks for the pattern matching script to use 

	:param low: telephone number in E164 format
	:type low: integer
	:param high: telephoen number in E164 format
	:type high: integer
	:returns: list of integer tuples for pattern chunking
	:rtype: list
	"""

	from dialplan_exceptions import DialplanException

	#start by ensuring our arguments are integers
	low = int(low)
	high = int(high)

	#get string representations of numbers
	fn_string = str(low)
	ln_string = str(high)

	if len(fn_string) != len(ln_string):
		#the pattern to match is not valid
		raise DialplanException("First and last numbers are not of equal length")

	if low > high:
		raise DialplanException("Last number is smaller than the first number")

	if low == high:
		return [(low, high)]

	patterns = []

	#lets work out the number of significant digits
	pattern = common_start(low,high)
	digit_start = int(len(pattern))
	digits = len(str(low)) - len(pattern)
	strip_digits = int(digits*-1)
	remaining_fn = fn_string[strip_digits:]
	remaining_ln = ln_string[strip_digits:]

	remaining_fn_int = int(remaining_fn)
	remaining_ln_int = int(remaining_ln)

	last_of_first_range = int(math.ceil(float(remaining_fn_int/math.pow(10,digits-1)))*math.pow(10,digits-1))

	first_of_last_range = int(math.floor(float((remaining_ln_int+1)/math.pow(10,digits-1)))*math.pow(10,digits-1))
	
	if remaining_fn_int != last_of_first_range:
		low = pattern+str(remaining_fn_int).zfill(int(digits))
		high = pattern+str(last_of_first_range-1).zfill(int(digits))
		if strip_digits == 1:
			patterns.append((int(low), int(high)))
		else:
			patterns.extend(split_range(int(low), int(high)))

	if last_of_first_range != first_of_last_range:
		#we have a range in the middle
		low = pattern+str(last_of_first_range).zfill(int(digits))
		high = pattern+str(first_of_last_range-1).zfill(int(digits))
		patterns.append((int(low), int(high)))

	if (first_of_last_range-1) != remaining_ln_int:
		low = pattern+str(first_of_last_range).zfill(int(digits))
		high = pattern+str(remaining_ln_int).zfill(int(digits))
		if strip_digits == 1 or low == high:
			patterns.append((int(low), int(high)))
		else:
			patterns.extend(split_range(int(low), int(high)))

	
	return patterns