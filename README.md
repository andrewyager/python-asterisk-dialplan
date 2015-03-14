# python-asterisk-dialplan

## Introduction
[Asterisk](http://www.asterisk.org/) is a very powerful IP PBX application, however it's dialplan logic can appear quite complicated.

This module adds some python bindings to help you manipulate patterns (and in future, more) from the dialplan. Initially, there is functions to help you "chunk" a range of numbers into asterisk dialplan patterns.

## Installation

You can install this by simply running:

```
pip install asterisk_dialplan
```

Or you can use the latest development version:

```
pip install -e git+git://github.com/andrewyager/python-asterisk-dialplan.git#egg=asterisk_dialplan
```

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

New in version 1.3 is support for parsing a dialplan context, and various functions to help determine what this context actually means. We support
extensions, numeric and "n" priorities and a few other nice things. At this stage we don't support named priorities; and these are likely ot break it.

The example below interprets a dialplan context, converts the extensions to ranges and finally determines the numeric coverage for these.

Note: This currently does not support patterns with "selective" ranges due to an incompleteness in the logic for creating patterns in patterns.py. This means that patterns such as _145X[12459] will not be correctly interpreted, and you will instead be treated as _145X[1-9].

Note that there is also currently no test coverage for this code. Contributions to resolve both of these issues are welcomed.

```
from asterisk_dialplan.dialplan import parse_diaplan_context, convert_dialplan_to_range, range_to_numbers

dialplan = """
exten => 1234,1,Dial(SIP/blah/${EXTEN})
exten => 1234,2,Hangup()
exten => _123415X,1,Dial(SIP/blah/${EXTEN},r)
exten => _123415X,n,Hangup
exten => _NXX,1,Dial(SIP/blah/${EXTEN})
same => n,Dial(SIP/blah/${EXTEN})
same = n, Dial(SIP/blah2/${EXTEN})
exten => s,1,Hangup
exten => t,1,Hangup
exten => i,Hangup
exten = _s14XX,1,Playback(invalid)
exten = _s14tXXy,1,Playback(invalid)
; this is a comment that will be ignored
"""

dialplan = parse_diaplan_context(dialplan)

print dialplan

dialplan = convert_dialplan_to_range(dialplan)

print dialplan


#now we print all of the individual numbers that make this up
for rule in dialplan:
  if 'exten_range' in rule:
    for exten_range in rule['exten_range']:
      extens = range_to_numbers(exten_range[0], exten_range[1])
      for exten in extens:
        print str(exten)
  else:
    print str(rule['exten'])
```

## Error Handling

If you provide bad input (i.e. your input strings/numbers aren't the same length, or your upper number is less than your lower number) the module will throw a DialplanException which you can handle.

The module only (currently) handles numeric matches, so while you can match on strings etc within Asterisk, it's not designed to handle anything like that. It also expects both arguments to be of the same length and in E.164 format (as indicated by the fact it will throw an exception).

If you provide numbers in a national format (perhaps with a leading 0?) this is currently untested and probably won't work properly.






