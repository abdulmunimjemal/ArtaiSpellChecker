import sys, threading, itertools
from utils.file_reader import read_file, read_lines
from ngram_model import NgramModel
from spell_checker import SpellChecker
import time

dictionary_path = 'data/amharic_dictionary.txt'

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
time.sleep(1)
done = True


def check(text):
    start_timestamp = time.time()
    result = spell_checker.check(text)
    end_timestamp = time.time()
    result["checking_time"] = f"{round(end_timestamp - start_timestamp, 2)} seconds"
    return result


if __name__ == "__main__":
    sample_amharic_text = """
    የቤት ውስጥ ስራ "የሴቶች ስራ" ብቻ ሳይቻሆን የሁሉም ሰው ሊሆን ይችላን።
    """
    result = check(sample_amharic_text)
    print(result)