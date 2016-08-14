"""
Determining the alphabet based on a list of words in alphabetical order.

Assumptions:
-the list of words contains enough words that to comprise the entire alphabet
-The alphabet contains any amount of letters and any distinct symbols
"""


def get_alphabet(words):
	'''
	Returns the alphabet from a list of words using the first letter only
	'''
	output = list()

	for word in words:
		if word[0] not in output:
			output.append(word[0])

	return output


def get_words_starting_with(word_list, letter):
	'''
	Returns words from list that start with a particular letter
	'''
	output = list()
	
	for w in word_list:
		if w[0] == letter and len(w) > 1:
			output.append(w[1:])

	return output


def update_dictionary(order_dict, list_alphabet):
	'''
	Update the order dictionary. The order dictionary specifies the letters
	that come BEFORE that particular key
	order_dict key: letter of alphabet
	order_dict value: letters that come before the key letter
	'''
	for ind in range(len(list_alphabet)):
		if list_alphabet[ind] not in order_dict:
			order_dict[list_alphabet[ind]] = set()
		newset = order_dict[list_alphabet[ind]].union(set(list_alphabet[0:ind]))
		order_dict[list_alphabet[ind]] = newset

	return order_dict


def get_order_dictionary(word_list, order_dict):
	'''
	Recursively finds all possible alphabets from a particular list of words
	and returns an updated order_dict
	'''
	if not word_list:
		return order_dict

	alphabet_letters = get_alphabet(word_list)
	order_dict = update_dictionary(order_dict, alphabet_letters)

	while (len(word_list) > 0):
		curr_letter = word_list[0][0]
		new_word_list = get_words_starting_with(word_list, curr_letter)
		while (len(word_list) > 0):
			if curr_letter == word_list[0][0]:
				word_list.pop(0)
			else:
				break

		order_dict = get_order_dictionary(new_word_list, order_dict)

	return order_dict


def get_alphabet_from_order(order_dict):
	final_alphabet = list()

	while (len(order_dict) > 0):
		empty_set_key = ""
		for letter, comes_after in order_dict.items():
			if comes_after == set():
				empty_set_key = letter

		final_alphabet.append(empty_set_key)
		del order_dict[empty_set_key]

		for l in order_dict:
			if empty_set_key in order_dict[l]:
				order_dict[l].remove(empty_set_key)

	return final_alphabet


if __name__ == "__main__":
	#read in words and strip spaces / new lines
	files = ['alphabet.txt', 'listnames.txt']

	for filename in files:
		print 'For file', filename
		with open(filename) as f:
		    word_list = f.readlines()
		    word_list = [x.strip('\n') for x in word_list]
		    word_list = [x.strip('\t') for x in word_list]
		    word_list = [x.strip(' ') for x in word_list]

		order_dict = dict()
		order_dict = get_order_dictionary(word_list, order_dict)

		final_alphabet = get_alphabet_from_order(order_dict)

		# print results to console
		for i in range(len(final_alphabet)):
			print 'Letter {0} -> {1}'.format(i + 1, final_alphabet[i])

		print 'Total number of letters: {0}'.format(len(final_alphabet))
		print ''
