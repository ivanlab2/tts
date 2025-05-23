""" from https://github.com/keithito/tacotron """
import re
from tacotron2.text import cleaners
from tacotron2.text.symbols import symbols


# Mappings from symbol to numeric ID and vice versa:
_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')

'''
#def text_to_sequence(text, cleaner_names):
  #sequence = []

  # Check for curly braces and treat their contents as ARPAbet:
  while len(text):
    m = _curly_re.match(text)
    if not m:
      sequence += _symbols_to_sequence(_clean_text(text, cleaner_names))
      break
    sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
    sequence += _arpabet_to_sequence(m.group(2))
    text = m.group(3)

  return sequence
'''

def text_to_sequence(text, cleaner_names):
    '''Converts text to a sequence of symbol IDs (no ARPAbet, for Russian TTS)'''
    cleaned_text = _clean_text(text, cleaner_names)
    return _symbols_to_sequence(cleaned_text)
'''
def sequence_to_text(sequence):
 # Converts a sequence of IDs back to a string
  result = ''
  for symbol_id in sequence:
    if symbol_id in _id_to_symbol:
      s = _id_to_symbol[symbol_id]
      # Enclose ARPAbet back in curly braces:
      if len(s) > 1 and s[0] == '@':
        s = '{%s}' % s[1:]
      result += s
  return result.replace('}{', ' ')
'''
def sequence_to_text(sequence):
    return ''.join([_id_to_symbol[symbol_id] for symbol_id in sequence if symbol_id in _id_to_symbol])

def _clean_text(text, cleaner_names):
  for name in cleaner_names:
    cleaner = getattr(cleaners, name)
    if not cleaner:
      raise Exception('Unknown cleaner: %s' % name)
    text = cleaner(text)
  return text


def _symbols_to_sequence(symbols):
  return [_symbol_to_id[s] for s in symbols if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
  return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s):
  return s in _symbol_to_id and s != '_' and s != '~'

