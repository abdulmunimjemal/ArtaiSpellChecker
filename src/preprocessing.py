import re
from utils.amharic_normalizer import AmharicNormalizer

def remove_non_amharic(text: str) -> str:
    """
    Remove non-Amharic characters from the text.
    """
    amharic_pattern = re.compile("[ሀ-ቿ]+")
    return "".join(amharic_pattern.findall(text))

def normalize(text: str) -> str:
    """
    Normalize Amharic Text
    """
    normalizer = AmharicNormalizer()
    return normalizer.normalize(text)
    

def preprocess_text(text: str) -> str:
    """
    Perform general preprocessing steps on the input text.
    """
    text = remove_non_amharic(text)
    text = normalize(text)

    return text
