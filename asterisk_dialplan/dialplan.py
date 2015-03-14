""" Dialplan Functions """

from patterns import pattern_to_ranges
import re

def parse_diaplan_context(dialplan_string):
  """ Build a dictionary that represents the given set of dialplan elements
  contained in this input string. The key in the dictionary corresponds to 
  the extension, and the arguments are priority followed by the command """

  rows = [s.strip() for s in dialplan_string.splitlines()]
  dialplan = {}
  exten = None
  priority = None
  grammar = re.compile(r"^(exten\s*?\=\>?\s*(?P<exten>.+)\s*,\s*(?P<priority>[0-9]+|n)\s*,\s*(?P<command>.+))|(same\s*?\=\>?\s*(?P<priority_same>[0-9]+|n)\s*,\s*(?P<command_same>.+))")

  for row in rows:
    result = grammar.search(row)
    if result:
      if result.group("exten"):
        if result.group("priority") == "n":
          priority += 1
        else:
          priority = int(result.group("priority"))
        exten = result.group("exten")
        command = result.group("command")
      else:
        if result.group("priority_same") == "n":
          priority += 1
        else:
          priority = int(result.group("priority_same"))
        command = result.group("command_same")
      if exten not in dialplan:
        dialplan[exten] = []
      if priority > len(dialplan[exten]):
        #we need to fill out the priority ot this point
        dialplan[exten].extend(range(len(dialplan[exten]), priority+1))
      dialplan[exten][priority-1] = command

  return dialplan

def convert_dialplan_to_range(dialplan):
  """ This function takes a dialplan dictionary (for example, as created
    by parse_dialplan_context) and retusn a dictionary containing the
    "low" and "high" values for the extension patterns.

    Due to this change, there is no longer a "key" but rather a property
    that either stores the single extension or a list of ranges.
    """
  new_dialplan = []
  for key,value in dialplan.iteritems():
    if key[0] == "_":
      dialplan_obj = {
        "exten_range": pattern_to_ranges(key),
        "args": value
      }
    else:
      dialplan_obj = {
        "exten": key,
        "args": value
      }
    new_dialplan.append(dialplan_obj)
  return new_dialplan

def range_to_numbers(start, end):
  """
  This function takes a "range" of numbers that corresponds to an
  Asterisk extension and returns a list of the valid numbers that
  match it. In the event that the range contains non-numeric digits
  the function will still return a valid interpretation of the pattern.
  """
  def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
  if RepresentsInt(start) and RepresentsInt(end):
    # we have a range
    return range(int(start), int(end)+1)

  # we have a complex range, so we need to be a bit more creative

  start_int = int(''.join(c for c in start if c in '0123456789'))
  end_int = int(''.join(c for c in end if c in '0123456789'))
  numeric_range = range(start_int, end_int+1)
  numbers = []
  for x in numeric_range:
    number = str(x)
    pos = 0
    exten = ""
    for character in start:
      if character in '0123456789':
        #we are eligable to replace this with a digit from our range
        exten += number[pos]
        pos = pos + 1
      else:
        exten += character
    numbers.append(exten)

  return numbers
