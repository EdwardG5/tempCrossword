from exceptions import DictError

# ENSURES: the returned list is clean, well formatted, all lowercase (duplicates possible)
def fileToWords(fileRoute):
	fp = open(fileRoute)
	words = fp.read().split()
	length = len(words)
	for x in range(length):
		words[x] = words[x].lower()
	for x in range(length):
		if not words[x].isalpha():
			raise DictError('Provided word list contains invalid strings:', words[x])
	fp.close()
	return words
