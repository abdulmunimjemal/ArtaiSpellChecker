from utils.amharic_tokenizer import AmharicSegmenter
from preprocessing import preprocess
from nltk.util import ngrams
import pickle

# ngram_model.py

class NgramModel:
    def __init__(self, corpus: str, ngram_size=3):
        self.corpus = corpus
        self.preprocess()
        self.tokenizer = AmharicSegmenter()
        self.ngram_size = ngram_size
        self.ngram_counts = defaultdict(int)
    
    def preprocess(self):
        self.corpus = preprocess(self.corpus)
        self.corpus = self.tokenizer.tokenize_sentence(self.corpus)
        
    def train(self):
        for sentence in self.corpus:
            words = self.tokenizer.tokenize(sentence)
            for ngram in ngrams(words, self.ngram_size):
                self.ngram_counts[ngram] += 1
    
    def get_ngram_count(self, ngram):
        return self.ngram_counts[ngram]
    
    def get_ngram_probability(self, ngram):
        ngram_count = self.get_ngram_count(ngram)
        total_count = sum(self.ngram_counts.values())
        return ngram_count / total_count

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    def get_ngram_probability_with_backoff(self, ngram):
        """
        ngram: (a, b, c) = (before, word, after)
        """ 
        ngram_count = self.get_ngram_count(ngram)
        total_count = sum(self.ngram_counts.values())
        if ngram_count == 0:
            return self.get_ngram_probability_with_backoff(ngram[1:])
        else:
            return ngram_count / total_count
    
    
    
    # def get_ngram_probability_with_smoothing(self, ngram):
    #     ngram_count = self.get_ngram_count(ngram)
    #     total_count = sum(self.ngram_counts.values())
    #     return (ngram_count + 1) / (total_count + len(self.ngram_counts))
    

    
    # def get_ngram_probability_with_interpolation(self, ngram):
    #     ngram_count = self.get_ngram_count(ngram)
    #     total_count = sum(self.ngram_counts.values())
    #     return (ngram_count + 1) / (total_count + len(self.ngram_counts))
    
    # def get_ngram_probability_with_good_turing(self, ngram):
    #     ngram_count = self.get_ngram_count(ngram)
    #     total_count = sum(self.ngram_counts.values())
    #     return (ngram_count + 1) / (total_count + len(self.ngram_counts))
    
    # def get_ngram_probability_with_kneser_ney(self, ngram):
    #     ngram_count = self.get_ngram_count(ngram)
    #     total_count = sum(self.ngram_counts.values())
    #     return (ngram_count + 1) / (total_count + len(self.ngram_counts))
    
    # def get_ngram_probability_with_witten_bell(self, ngram):
    #     ngram_count = self.get_ngram_count(ngram)
    #     total_count = sum(self.ngram_counts.values())
    #     return (ngram_count + 1) / (total_count + len(self.ngram_counts))
    
    # def get_ngram_probability_with_absolute_discounting(self, ngram):
    #     ngram_count = self.get_ngram_count(ngram)
    #     total_count = sum(self.ngram_counts.values())
    #     return (ngram_count + 1) / (total_count + len(self.ngram_counts))
    
    
    