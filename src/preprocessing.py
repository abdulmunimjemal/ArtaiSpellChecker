import re
from utils.amharic_normalizer import AmharicNormalizer

class AmharicTextProcessor:
    def __init__(self):
        self.normalizer = AmharicNormalizer()
        self.amharic_pattern = re.compile('[ሀ-፼ ]+')

    def remove_non_amharic(self, text: str) -> str:
        """
        Remove non-Amharic characters from the text.
        """
        matches = self.amharic_pattern.findall(text)
        cleaned_text = ''.join(matches)
        return cleaned_text

    def normalize(self, text: str) -> str:
        """
        Normalize Amharic Text
        """
        return self.normalizer.normalize(text)

    def preprocess(self, text: str) -> str:
        """
        Perform general preprocessing steps on the input text.
        """
        text = self.normalize(text)
        text = self.remove_non_amharic(text)
        return text

