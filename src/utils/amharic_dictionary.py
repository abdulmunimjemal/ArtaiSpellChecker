from utils.file_reader import read_lines 
from collections import defaultdict

class Dictionary:
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path
        self.dictionary = defaultdict(lambda: 0)
        
        dictionary = read_lines(self.dictionary_path)
        for word in dictionary:
            self.dictionary[word] += 1
    
    def __contains__(self, word):
        return self.dictionary[word] != 0
    
    def look(self, word):
        return self.dictionary[word] != 0