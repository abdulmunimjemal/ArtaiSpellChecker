from utils.file_reader import read_file, read_lines
from preprocessing import preprocess
from utils.amharic_tokenizer import AmharicSegmenter
from spell_checker import SpellChecker

dictionary_path = 'data/amharic_dictionary.txt'
corpus_path = 'data/amharic_corpus.txt'

# corpus = read_file(corpus_path)
# corpus = preprocess(corpus)

# tokenizer = AmharicSegmenter()
# corpus = tokenizer.tokenize_sentence(corpus)

# ngram_size = 3

print("STARTING SPELL CHECKER ENGINIE")
def main():
    spell_checker = SpellChecker(dictionary_path)

    # Example usage
    word_to_check = "ሴጅት"  # Replace with the word you want to check 
    is_spelled_correctly = spell_checker.check_spelling(preprocess(word_to_check))

    if is_spelled_correctly:
        print(f"The word '{word_to_check}' is spelled correctly.")
    else:
        suggestions = spell_checker.suggest_corrections(word_to_check)
        print(
            f"The word '{word_to_check}' is misspelled. Suggestions: {suggestions}")


if __name__ == "__main__":
    main()
