import re
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS


def remove_special_characters(text):
    return re.sub('[^a-zA-Z0-9 ]', '', text)


def remove_stop_words_and_tokenize(text):
    return remove_stopwords(text.lower()).split(" ")
