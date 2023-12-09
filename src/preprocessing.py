import re
from utils.amharic_normalizer import AmharicNormalizer

def remove_non_amharic(text: str) -> str:
    """
    Remove non-Amharic characters from the text.
    """
    amharic_pattern = re.compile('[ሀ-፼ ]+')
    matches = amharic_pattern.findall(text)
    cleaned_text = ''.join(matches)
    return cleaned_text
   
def normalize(text: str) -> str:
    """
    Normalize Amharic Text
    """
    normalizer = AmharicNormalizer()
    return normalizer.normalize(text)
    

def preprocess(text: str) -> str:
    """
    Perform general preprocessing steps on the input text.
    """
    text = normalize(text)
    text = remove_non_amharic(text)
    
    return text
