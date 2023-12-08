# spell_checker.py
from damerau_levenshtein import damerau_levenshtein_distance
from ngram_model import build_ngram_model, generate_ngrams

class SpellChecker:
    def __init__(self, corpus, ngram_size, dictionary_path):
        self.corpus = corpus
        self.ngram_size = ngram_size
        self.ngram_model = build_ngram_model(corpus, ngram_size)
        self.dictionary = Dictionary(dictionary_path)

    def suggest_corrections(self, word, num_suggestions=7):
        """
        Suggest corrections for the given word.
        """
        # Your implementation goes here
        suggestions = []
        word_ngrams = generate_ngrams(word, self.ngram_size)
        
        for candidate in self.corpus:
            candidate_ngrams = generate_ngrams(candidate, self.ngram_size)
            intersection = set(word_ngrams) & set(candidate_ngrams)
            jaccard_similarity = len(intersection) / len(set(word_ngrams) | set(candidate_ngrams))
            
            suggestions.append((candidate, jaccard_similarity))
        
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [suggestion[0] for suggestion in suggestions[:num_suggestions]]

    def check_spelling(self, word, threshold=0.8):
        """
        Check the spelling of the given word.
        """
        result = self.dictionary.look(word)
        if result:
            return True
        
        for candidate in self.corpus:
            distance = damerau_levenshtein_distance(word, candidate)
            similarity = 1 - distance / max(len(word), len(candidate))
            if similarity > threshold:
                return True
        return False