import json

# Filter an array of strings to meet specific parameters
def filter_terms(array):
	return [term.lower() for term in array if term.isalpha()]

# Return a json file as an array/object
def load_json(filename = 'terms'):
	with open(f'files/{filename}.json', 'r') as json_file:
		return json.load(json_file)

# Return a text file as an array of its lines
def load_txt(filename = 'terms'):
	with open(f'files/{filename}.txt', 'r') as txt_file:
		return [line.rstrip('\n') for line in txt_file]

# Remove a specific term from the terms file
def remove_term(term):
	print(f'Removing the term | {term}')
	terms = load_json()
	terms.remove(term)
	write_json(terms)

# Reset the terms.json file to consist of all the terms in the terms-all.txt file (after filtering)
def reset_terms():
	terms = filter_terms(load_txt())
	write_json(terms)

# Write an array/object to a json file
def write_json(data, filename = 'terms'):
	with open(f'files/{filename}.json', 'w') as json_file:
		json.dump(data, json_file, indent = 2)
