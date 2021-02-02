import inflect
import re

# Initialise the inflect engine
engine = inflect.engine()

# Returns text with 'a' or 'an' proceeding it
def a_or_an(text):
	return engine.a(text)

# Capitalise the first letter of each word in given text
def capitalise(text):
	if len(text) < 3:
		return text.upper()
	else:
		return ' '.join(f'{word[0].upper()}{word[1:]}' for word in text.split(' '))

# Converts a number into its multiplicative form
def convert_num_to_multiplicative(num):
	if num == 1:
		return 'once'
	elif num == 2:
		return 'twice'
	elif num == 3:
		return 'thrice'
	else:
		return f'{convert_num_to_words(num)} times'

# Converts a number into readable text
def convert_num_to_words(num):
	return engine.number_to_words(num, andword = '')

# Format object keys into readable text
def format_key(key):
  return capitalise(re.sub(r'_', ' ', key))

# Returns the pluralised version of passed text
def pluralise(text):
	return engine.plural(text)

# Replace all multi-char spaces with a single char space
def remove_multi_spaces(text):
	return re.sub(r'  +', ' ', text, 0).strip()

# Convert the first character in a string to uppercase
def upper(text):
	if len(text) > 1:
		return f'{text[0].upper()}{text[1:]}'
	else:
		return text.upper()
