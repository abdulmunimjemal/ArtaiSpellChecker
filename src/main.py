import sys
import threading
import itertools
from utils.file_reader import read_file, read_lines
from preprocessing import preprocess
from utils.amharic_tokenizer import AmharicSegmenter
from spell_checker import SpellChecker
from collections import defaultdict
import time

dictionary_path = 'data/amharic_dictionary.txt'
corpus_path = 'data/amharic_corpus.txt'
tokenizer = AmharicSegmenter()

# corpus = read_file(corpus_path)
# corpus = preprocess(corpus)

# corpus = tokenizer.tokenize_sentence(corpus)

# ngram_size = 3


done = False


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r Loading Dictionary ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone Loading!')


t = threading.Thread(target=animate)
t.start()
spell_checker = SpellChecker(dictionary_path)
time.sleep(2)
done = True


def check(text):
    start_timestamp = time.time()
    result = {
        "text": text,
        "corrected_text": "",
        "errors": {}
    }
    corrected_text = text  # using the first suggestions
    text = preprocess(text)
    print(text)
    sentences = tokenizer.tokenize_sentence(text)
    for sentence in sentences:
        words = tokenizer.tokenize(sentence)
        for word in words:
            if not spell_checker.check_spelling(word):
                suggestions = spell_checker.suggest_corrections(word)
                result["errors"][word] = suggestions
    # generate corrected text
    for error, suggestions in result["errors"].items():
        if suggestions:
            corrected_text = corrected_text.replace(error, suggestions[0])
    result["corrected_text"] = corrected_text
    end_timestamp = time.time()
    result["checking_time"] = f"{round(end_timestamp - start_timestamp, 2)} seconds"
    return result

if __name__ == "__main__":
    sample_amharic_text = """
    የቤት ውስጥ ስራ "የሴቶች ስራ" ብቻ ሳይቻሆን የሁሉም ሰው ሊሆን ይችላን።
    """
    result = check(sample_amharic_text)
    for key, value in result.items():
        print(f"{key}   ---- {value}")
