from .file import load_json
from .string import a_or_an, remove_multi_spaces, upper
from datetime import date
import random
import re

# Returns a greeting specifically calibrated to the user's data
def generate_greeting(user, max_length, error = False):
	def adjective_sub(text):
		adjective = a_or_an(random.choice(greetings['Adjectives'][secondary]))
		return re.sub(r'\[adjective\]', adjective, text, 0)

	def form_into_phrase(array):
		if type(array) == list:
			selections = [random.choice(arr) for arr in array]
			value = ' '.join(selections)
		else:
			value = array
		return adjective_sub(version_sub(upper(remove_multi_spaces(value.strip()))))

	def version_sub(text):
		today = date.today()
		version = f'{today.year}.{today.month}.{today.day}'
		return re.sub(r'\[version\]', version, text, 0)

	# Save the greetings file to memory
	greetings = load_json('greetings')

	# Find the primary key based on the users status
	primary = 'Chad' if user.is_chad else 'Virgin'

	# Find the secondary key
	secondary = 'Formal' if user.is_verified else 'Informal'		

	# Create an array containing the selected greeting
	main_selection = random.choice(greetings[primary][secondary])
	main_greeting = form_into_phrase(main_selection)
	sections = [main_greeting]
	
	# If today is the users cake day, adjust the greeting to reflect that
	if user.is_cake_day:
		cd_selection = greetings['Cake Day'][secondary]
		cd_greeting = form_into_phrase(cd_selection)
		sections.append(cd_greeting)
	
	# Convert the array into a string with a newline between each element
	try:
		greeting = '\n'.join(sections).format(user.username)
	# Catch an error when attempting to format a greeting without '{}'
	except ValueError:
		greeting = 'oof'

	# If the greeting is too long to be tweeted or the user's username is not in the tweet,
	# fall back on an error greeting (happens when the above formatting error also occurs)
	if error or len(greeting) >= max_length or not(user.username in greeting):
		return form_into_phrase(random.choice(greetings['Error'])).format(user.username)
	else:
		return greeting

# Returns a random term from the terms file
def get_random_term():
	terms = load_json('terms')
	return random.choice(terms)
