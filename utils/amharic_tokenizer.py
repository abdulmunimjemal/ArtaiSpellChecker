import re
from typing import List

class AmharicSegmenter:
    def __init__(self, sent_punct=None, word_punct=None):
        self.SENT_PUNC = sent_punct or ["።", "፥", "፨", "::", "፡፡", "?", "!"]
        self.WORD_PUNC = word_punct or ["።", "፥", "፤", "፨", "?", "!", ":", "፡", "፦", "፣"]

    def amharic_tokenizer(self, text: str) -> List[str]:
        """
        Tokenizer based on space character and different Amharic punctuation marks only.
        """
        tokens = []
        word = ""
        prev_char = ''
        
        for index, char in enumerate(text):
            if char == " ":
                if word:
                    tokens.append(word)
                word = ""
            elif char in self.WORD_PUNC:
                if word and prev_char != char:
                    tokens.append(word)
                    word = ""
                prev_char = char
                word += char
            else:
                word += char
        
        if word:
            tokens.append(word)
        
        return tokens

    def find_all(self, punct, text):
        return [i + len(punct) - 1 for i in range(len(text)) if text.startswith(punct, i)]

    def tokenize_sentence(self, text: str) -> List[str]:
        text = re.sub("\n", "።", text)
        text = re.sub("\s+", " ", text)
        
        tokenized_text = []
        idxs = [-1]
        
        for sep in self.SENT_PUNC:
            idxs.extend(self.find_all(sep, text))

        idxs = sorted(idxs)
        
        if len(idxs) == 1:
            tokenized_text.append(text)  # just one sentence without the punctuation marks
            
        for i in range(len(idxs) - 1):
            tokenized_text.append(text[idxs[i] + 1 : idxs[i + 1] + 1].strip())
        
        return tokenized_text

    def window_lines(self, line, window):
        '''
        Some models require the length of the sentence to be moderate, so to avoid shorter sentences, append some using some windowing technique
        '''
        try:
            text = re.sub("\s+", " ", line)
            sentences = [s for s in self.tokenize_sentence(text) if len(s) >= 6]
            windowed_sentences = [" ".join(sentences[snt : snt + window]) for snt in range(len(sentences))]
            return windowed_sentences
        except Exception as e:
            print(f"Could not parse line \n{line}\n")
            return []

    def window_sents(self, sentences, window):
        '''
        Some models require the length of the sentence to be moderate, so to avoid shorter sentences, append some using some windowing technique
        '''
        try:
            windowed_sentences = [" ".join(sentences[snum : snum + window]) for snum in range(len(sentences))]
            return windowed_sentences
        except Exception as e:
            print(f"Could not parse sentences \n{sentences}\n")
            return []
