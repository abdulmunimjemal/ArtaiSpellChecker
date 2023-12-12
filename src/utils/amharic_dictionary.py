from utils.file_reader import read_lines
from collections import defaultdict
from utils.amharic_normalizer import AmharicNormalizer

# TODO: Serialize the dictionary object to a file option

normalizer = AmharicNormalizer()

class Dictionary:
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path
        self._dictionary = defaultdict(lambda: 0)
        dictionary = read_lines(self.dictionary_path)
        for word in dictionary:
            self._dictionary[normalizer.normalize(word)] += 1
        self._dictionary_words = self._dictionary.keys()

    def __contains__(self, word):
        return self._dictionary[word] != 0

    def look(self, word):
        return self._dictionary[word] != 0

    def get_words(self):
        return self._dictionary.keys()
