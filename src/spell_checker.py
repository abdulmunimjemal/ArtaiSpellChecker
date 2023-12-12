# for PoS Tagging
from flair.models import SequenceTagger
from flair.data import Sentence

# Distance Calculation and Dictionary Look Up
from damerau_levenshtein import levenshtein_distance
from utils.amharic_dictionary import Dictionary

# Text Preprocessing
from preprocessing import AmharicTextProcessor
from utils.amharic_tokenizer import AmharicSegmenter

# Context Analyzer
from ngram_model import NgramModel

# utility
import pickle, os


# get absolute path of the model (one file up from the current directory)

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))[:-1])
bigram_model_path = current_dir + '/models/bigram_model_001.pkl'
pos_model_path = current_dir + '/models/am_pos_model.pt'
ngram_model = pickle.load(open(bigram_model_path, 'rb'))

# TODO: Serialize the dictionary object to a file option and use it here instead of direct loading

preprocess = AmharicTextProcessor().preprocess
class SpellChecker:
    def __init__(self, dictionary_path, ngram_model: NgramModel = ngram_model):
        self.dictionary = Dictionary(dictionary_path)
        self.model = ngram_model
        self.tokenizer = AmharicSegmenter()

    def _suggest_corrections(self, word, num_suggestions=7, threshold=0.75):
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
            "errors": []
        }
        preprocessed_text = preprocess(text)
        sentences = self.tokenizer.tokenize_sentence(preprocessed_text)

        offset = 0  # this is used to keep track of the index of the word in the original text

        for sentence in sentences:
            words = self.tokenizer.tokenize(sentence)
            for i, word in enumerate(words):
                if not self._check_spelling(word):
                    suggestions = self._suggest_corrections(word)

                    original_index = text.find(word, offset)
                    # update the offset to the end of the current word
                    offset = original_index + len(word)
                    adjacent_words = (
                        words[i-1] if i > 0 else None, words[i+1] if i < len(words) - 1 else None)
                    result["errors"].append({
                        'word': word,
                        'suggestions': suggestions,
                        'index': [original_index, original_index + len(word)],
                        'adjacent_words': adjacent_words,
                    })

        return self._rank_suggestions(result)

    def _rank_suggestions(self, dictionary_result):
        result = {
            'text': dictionary_result['text'],
            'errors': []
        }

        for error in dictionary_result["errors"]:
            word = error["word"]
            suggestions = error["suggestions"]
            index = error["index"]
            adjacent_words = error["adjacent_words"]
            ranked_suggestions = self._rank_individual_suggestions(
                word, suggestions, adjacent_words)

            result["errors"].append({
                'word': word,
                'suggestions': ranked_suggestions,
                'index': index,
            })

        return result

    def _calculate_relevance_score(self, suggestion, adjacent_words):
        """
        Calculate the relevance score of the given suggestions based on the adjacent words.
        """
        if adjacent_words[0] is not None:  # before provided
            return self.model.get_ngram_probability((adjacent_words[0],) + (suggestion,))
        elif adjacent_words[1] is not None:  # after provided
            return self.model.get_ngram_probability((suggestion,) + (adjacent_words[1],))
        else:
            return self.model.get_ngram_probability((suggestion,))

    def _rank_individual_suggestions(self, wrong_word, suggestions, adjacent_words):
        """
        Rank the given suggestions for the given wrong word.
        """
        if len(suggestions) <= 1:
            return suggestions

        ranked_suggestions = []
        scores = [self._calculate_relevance_score(
            suggestion, adjacent_words) for suggestion in suggestions]
        for i in range(len(suggestions)):
            ranked_suggestions.append((suggestions[i], scores[i]))
        ranked_suggestions = sorted(
            ranked_suggestions, key=lambda x: x[1], reverse=True)

        return [suggestion[0] for suggestion in ranked_suggestions]


class SpellCheckerWithPOS(SpellChecker):
    def __init__(self, dictionary_path, ngram_model: NgramModel = model, pos_model_path=pos_model_path):
        super().__init__(dictionary_path, ngram_model)
        self.pos_model = SequenceTagger.load(
            pos_model_path) if pos_model_path else None

    def _get_pos_tags(self, sentence):
        """
        Get POS tags for a given sentence.
        """
        if self.pos_model:
            flair_sentence = Sentence(sentence)
            self.pos_model.predict(flair_sentence)
            # get pos tags from the flair sentence
            return [token.to_dict()['labels'][0]['value'] for token in flair_sentence]

        else:
            # If POS model is not provided, return None for all POS tags
            return [None] * len(sentence.split())

    def check(self, text):
        result = {
            "text": text,
            "errors": []
        }
        preprocessed_text = preprocess(text)
        sentences = self.tokenizer.tokenize_sentence(preprocessed_text)

        for sentence in sentences:
            words = self.tokenizer.tokenize(sentence)
            pos_tags = self._get_pos_tags(sentence)

            for i, (word, pos_tag) in enumerate(zip(words, pos_tags)):
                # Skip checking nouns (NOUN) and pronouns (PRON)
                if pos_tag and pos_tag in {'NOUN', 'PRON'}:
                    continue

                if not self._check_spelling(word):
                    suggestions = self._suggest_corrections(word)

                    original_index = text.find(word)
                    adjacent_words = (
                        words[i - 1] if i > 0 else None, words[i + 1] if i < len(words) - 1 else None)

                    result["errors"].append({
                        'word': word,
                        'suggestions': suggestions,
                        'index': [original_index, original_index + len(word)],
                        'adjacent_words': adjacent_words,
                    })

        return self._rank_suggestions(result)
