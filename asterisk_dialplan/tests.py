""" Unit tests for asterisk dialplan functions """

import patterns
import ranges
import unittest
from dialplan_exceptions import DialplanException


class rangeChunks(unittest.TestCase):
	chunks = (
			#range of integers with rollover sections
			((61290370463, 61290373598), 
				[(61290370463, 61290370469),
				(61290370470, 61290370499),
				(61290370500, 61290370999),
				(61290371000, 61290372999),
				(61290373000, 61290373499),
				(61290373500, 61290373589),
				(61290373590, 61290373598)]
			),
			#rollover digits
			((61212349993, 61212350012),
				[(61212349993, 61212349999),
				(61212350000, 61212350009),
				(61212350010, 61212350012)]
			),
			#small rollover with only high and low
			((61212349993, 61212350002),
				[(61212349993, 61212349999),
				(61212350000, 61212350002)]
			),
			#small rollover with only middle and high ranges
			((61212349990, 61212350002),
				[(61212349990, 61212349999),
				(61212350000, 61212350002)]
			),
			# tiny small range
			((61290370463, 61290370469),
				[(61290370463, 61290370469)]
			),
			# equal start and end numbers
			((61290370463, 61290370463),
				[(61290370463, 61290370463)]
			),
			# string input
			(("61290370463", "61290370463"),
				[(61290370463, 61290370463)]
			),
	)


	def testRangeToChunk(self):
		"""ranges.split_range should give known results for these known inputs"""
		for numbers,split in self.chunks:
			result = ranges.split_range(numbers[0],numbers[1])
			self.assertEqual(result, split)

class rangeChunkBadInput(unittest.TestCase):
	def testLowBiggerThanHigh(self):
		"""split_range should fail if low is larger than high"""

		self.assertRaises(DialplanException, ranges.split_range, 61290373598 ,61290370463)

	def testUnequalSourceLength(self):
		"""split_range should fail if the two numbers aren't of equal length"""
		import dialplan_exceptions as ast_exception

		self.assertRaises(DialplanException, ranges.split_range, 1 , 30)

class patternChunks(unittest.TestCase):
	chunks = (
			#range of integers with rollover sections
			((61290370463, 61290373598), 
				["_6129037046[3-9]",
				"_612903704[7-9]X",
				"_61290370[5-9]XX",
				"_6129037[1-2]XXX",
				"_61290373[0-4]XX",
				"_612903735[0-8]X",
				"_6129037359[0-8]"]
			),
			#rollover digits
			((61212349993, 61212350012),
				["_6121234999[3-9]",
				"_6121235000X",
				"_6121235001[0-2]"]
			),
			#small rollover with only high and low
			((61212349993, 61212350002),
				["_6121234999[3-9]",
				"_6121235000[0-2]"]
			),
			#small rollover with only middle and high ranges
			((61212349990, 61212350002),
				["_6121234999X",
				"_6121235000[0-2]"]
			),
			# tiny small range
			((61290370463, 61290370469),
				["_6129037046[3-9]"]
			),
			# equal start and end numbers
			((61290370463, 61290370463),
				["61290370463"]
			),
			# pattern for a Z
			((61290370461, 61290370469),
				["_6129037046Z"]
			),
			# pattern for a N
			((61290370462, 61290370469),
				["_6129037046N"]
			),
	)


	def testRangeToChunk(self):
		"""ranges.split_range should give known results for these known inputs"""
		for numbers,split in self.chunks:
			result = patterns.generate_patterns(numbers[0],numbers[1])
			self.assertEqual(result, split)

	def checkCoverage(self):
		for numbers,split in self.chunks:
			result = util.test_block_for_coverage(split, numbers[0], numbers[1])
			self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()