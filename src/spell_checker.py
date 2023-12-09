# spell_checker.py
from damerau_levenshtein import levenshtein_distance
from utils.amharic_dictionary import Dictionary

class SpellChecker:
    def __init__(self, dictionary_path, corpus=None,ngram_size=3):
        self.dictionary = Dictionary(dictionary_path)

    def suggest_corrections(self, word, threshold=0.65, num_suggestions=5):
        """
        Suggest corrections for the given word based on levenshtein distance.
        """
        suggestions = []

        for candidate in self.dictionary.get_words():
            distance = levenshtein_distance(word, candidate)
            similarity = 1 - distance / max(len(word), len(candidate))
            if similarity > threshold:
                suggestions.append(candidate)
        return suggestions[:num_suggestions]

    def check_spelling(self, word, threshold=0.99):
        """
        Check the spelling of the given word.
        """
        return self.dictionary.look(word)
        # if result:
        #     return True
        
        # # for candidate in self.dictionary.get_words():
        # #     distance = levenshtein_distance(word, candidate)
        # #     similarity = 1 - distance / max(len(word), len(candidate))
        # #     if similarity > threshold:
        # #         return True
        # return False