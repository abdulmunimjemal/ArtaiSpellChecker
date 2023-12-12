# spell_checker.py
from damerau_levenshtein import levenshtein_distance
from utils.amharic_dictionary import Dictionary
from preprocessing import preprocess
from utils.amharic_tokenizer import AmharicSegmenter
from ngram_model import NgramModel
import pickle, os

# get absolute path of the model (one file up from the current directory)

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))[:-1])
model_path = current_dir + '/models/bigram_model_001.pkl'
print(model_path)
model = pickle.load(open(model_path, 'rb'))

class SpellChecker:
    def __init__(self, dictionary_path, ngram_model: NgramModel = model):
        self.dictionary = Dictionary(dictionary_path)
        self.model = ngram_model
        self.tokenizer = AmharicSegmenter()

    def _suggest_corrections(self, word, num_suggestions=7, threshold=0.7):
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

    def _check_spelling(self, word):
        """
        Check the spelling of the given word.
        """
        return self.dictionary.look(word)
    
    def check(self, text):
        result = {
            "text": text,
            "errors": {}
        }
        text = preprocess(text)
        sentences = self.tokenizer.tokenize_sentence(text)
        for sentence in sentences:
            words = self.tokenizer.tokenize(sentence)
            i = 0
            for word in words:
                if not self._check_spelling(word):
                    suggestions = self._suggest_corrections(word)
                    result["errors"][word] = {
                        'sentence': sentence,
                        'tokenized': words,
                        'suggestions': suggestions,
                        'index': i}
                i += 1
        return self._rank_suggestions(result)
    
    def _rank_suggestions(self, dictionary_result):
        result = {}
        
        for error, suggestion in dictionary_result["errors"].items():
            wrong_word = error
            sentence = suggestion["sentence"]
            index = suggestion["index"]
            words = suggestion["tokenized"]
            suggestions = suggestion["suggestions"]
            
            ngram = []
            if len(words) == index-1 and len(words) > 1:
                # the word is at the end of the sentence
                before_word = words[index-1]
                suggestions = sorted(suggestions, key=lambda x: model.get_ngram_probability((before_word,) + (x,)), reverse=True)
            elif index == 0 and len(words) > 1:
                # the word is at the beginning of the sentence
                after_word = words[index+1]
                suggestions = sorted(suggestions, key=lambda x: model.get_ngram_probability((x,) + (after_word,)), reverse=True)
            elif len(words) == 1:
                pass
            else:
                before_word = words[index-1] # we will use this to rank the suggestions
                # after_word = words[index+1]
                suggestions = sorted(suggestions, key=lambda x: model.get_ngram_probability((before_word,) + (x,)), reverse=True)
                
            
            word_result = {
                'sentence': sentence,
                'suggestions': suggestions,
            }
            
            result[wrong_word] = word_result
        
        return result

