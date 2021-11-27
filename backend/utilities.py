import re
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from nltk.tokenize import word_tokenize


def remove_special_characters(text):
    return re.sub('[^a-zA-Z0-9 ]', '', text)


def remove_stop_words_and_tokenize(text):
    return remove_stopwords(text.lower())

def tokenize_str(text):
    # 1. Tokenization
    # 2. Removing special characters
    # 3. Removing stop words
    # 4. Normalization
    # 5. Stemming
    pass
