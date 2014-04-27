# python-asterisk-dialplan

## Introduction
[Asterisk](http://www.asterisk.org/) is a very powerful IP PBX application, however it's dialplan logic can appear quite complicated.

This module adds some python bindings to help you manipulate patterns (and in future, more) from the dialplan. Initially, there is functions to help you "chunk" a range of numbers into asterisk dialplan patterns.

## Installation

You can install this by simply running:

`pip install asterisk_dialplan`

Or you can use the latest development version:

`pip install -e git+git://github.com/andrewyager/python-asterisk-dialplan.git#egg=asterisk_dialplan`

## Usage

`asterisk_dialplan` contains two main modules you want to interact with, namely `ranges` and `patterns`.

`ranges` contains the functionality required to chunk a number set in E.164 format into the subset of ranges Asterisk needs to parse. `patterns` contains the functionality to convert numeric ranges into Asterisk dialplan patterns.

Example usage:

```
from asterisk_dialplan.patterns import generate_patterns

# A relatively boring example that produces the patterns
# _61290000[0-3]XX
patterns = generate_patterns("61290000000", "61290000399")

# A more interesting example that produces the patterns
# _6129000029[3-9], _612900003XX
patterns = generate_patterns("61290000293", "61290000399")

# A single string number may as well not be a pattern match
# because Asterisk is better if it does less work
#61290000299
patterns = generate_patterns(61290000299, 61290000299)
```

You can also use the ranges module to just split the range (perhaps you want to build phone dialplans and need similar logic)

```
from asterisk_dialplan.ranges import split_range
ranges = split_range("61290000000", "61290000399")
```

## Error Handling

If you provide bad input (i.e. your input strings/numbers aren't the same length, or your upper number is less than your lower number) the module will throw a DialplanException which you can handle.

The module only (currently) handles numeric matches, so while you can match on strings etc within Asterisk, it's not designed to handle anything like that. It also expects both arguments to be of the same length and in E.164 format (as indicated by the fact it will throw an exception).

If you provide numbers in a national format (perhaps with a leading 0?) this is currently untested and probably won't work properly.






