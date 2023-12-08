from utils.amharic_tokenizer import AmharicSegmenter

# ngram_model.py

def generate_ngrams(tokens: str, n: int) -> list:
    """
    Generate a list of n-grams from the given text.
    """
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = tokens[i:i+n]
        ngrams.append(ngram)
    return ngrams


# ngram_model.py

def build_ngram_model(corpus: list, n: int) -> dict:
    """
    Build an N-gram model from the given list of corpus.
    """
    ngram_model = {}
    tokenizer = AmharicSegmenter()
    if type(corpus) == str:
        corpus = tokenizer.tokenize_sentence(corpus)
    for sentence in corpus:
        sentence = tokenizer.tokenize(sentence)
        ngrams = generate_ngrams(sentence, n)
        for ngram in ngrams:
            if ngram in ngram_model:
                ngram_model[" ".join(ngram)] += 1
            else:
                ngram_model[" ".join(ngram)] = 1
    return ngram_model