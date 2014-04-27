def common_start(first_number, last_number):
	""" Get the common starting characters of the two strings first_number and last_number """
	str_first = str(first_number)
	str_last = str(last_number)
	common = ""
	for a,b in zip(list(str_first), list(str_last)):
		if a == b:
			common = common + a
		else:
			return common
	return None

def test_block_for_coverage(patterns, first_number, last_number):
	""" Helper function to allow testing for contiguous coverage of a block of numbers with a given set of patterns """
	patternList = []

	#convert patterns to regular expressions
	for pattern in patterns:
		pattern = re.sub(r'X', '\\d', pattern)
		pattern = re.sub(r'Z', '[1-9]', pattern)
		pattern = re.sub(r'N', '[2-9]', pattern)
		pattern = re.sub(r'^_', '', pattern)
		patternList.append(pattern)
	
	pre = re.compile("^("+"|".join(patternList)+")$")
	
	#test each number in range for 
	for x in range(int(first_number), int(last_number)+1):
		result = pre.match(str(x))
		if result is None:
			return False

	return True