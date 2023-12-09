# Artai Spell Checker

Artai Spell Checker is a simple spell checker implemented in Python. It uses a combination of Damerau-Levenshtein distance and N-gram models to check and suggest corrections for misspelled words. It is done as a group course project.

- **Campus**: Addis Ababa Institue of Technology.
- **Department**: Software and Information Technology Engineering
- **Course**: Fundamentals of Software Engineering I.
- **Advisor**: Instructor Nuniyat Kifle

Group Members

1.	Abdulmunim Jundurahman      UGR/8625/14
2.	Bisrat Asaye                UGR/8508/14
3.	Ezana Kifle                 UGR/4189/14
4.	Fuad Mohammad               UGR/6052/14
5.	Sifan Fita                  UGR/8856/14
6.	Yordanos Zegeye             UGR/6316/14


## Features

- Damerau-Levenshtein distance 
- N-gram model for contextualization


## Getting Started

### Prerequisites

- Python 3.x
- Required dependencies (specified in `requirements.txt`)

### Installation

```bash
pip install -r requirements.txt
```

### Usage 
1. Clone this repository
```bash
git clone https://github.com/abdulmunimjemal/ArtaiSpellChecker.git
cd ArtaiSpellChecker
```
2. Run the spell checker
```bash
cd src
python main.py
```
## File Structure

- **artai_spell_checker/**
  - **src/**
    - `__init__.py`: Initialization file for the `spell_checker` module.
    - `spell_checker.py`: Implementation of the `SpellChecker` class.
    - `damerau_levenshtein.py`: Implementation of the Damerau-Levenshtein distance.
    - `ngram_model.py`: Implementation of N-gram model functions.
    - **utils/**
      - `__init__.py`: Initialization file for the `utils` module.
      - `file_reader.py`: Implementation of file reading functions.
      - `amharic_tokenizer.py`: Implementation of an Amharic tokenizer.
      - `amharic_normalizer.py`: Implementation of an Amharic normalizer.
      - `amharic_dictionart.py`: Implementation of an Amharic Dictionary for Word Lookup.
    - `main.py`: Main script for running the spell checker.
    - `user_interface.py`: (Optional) Implementation of a user interface.
    - `preprocessing.py`: Implementation of Amahric text preprocessing functions.
    - `requirements.txt`: List of project dependencies.
    - `README.md`: Project documentation.

- **data/**
  - `amharic_dictionary.txt`: Dictionary file with Amharic words.
  - `amharic_corpus.txt`: Corpus file with Amharic sentences.

- `LICENSE`: Project license file.
