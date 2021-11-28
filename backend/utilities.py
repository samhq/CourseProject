import re
from gensim.parsing.preprocessing import remove_stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


def remove_special_characters(lst):
    lst1 = list()
    for element in lst:
        strs = re.sub('[^a-zA-Z0-9 ]', '', element)
        lst1.append(strs)
    return lst1


def stemming(lst):
    lst1 = list()
    ps = PorterStemmer()
    for word in lst:
        lst1.append(ps.stem(word))

    return lst1


def tokenize_str(text):
    # 1. Removing stop words
    text = remove_stopwords(text.lower())

    # 2. Tokenization
    words = word_tokenize(text)

    # 3. Removing special characters
    words = remove_special_characters(words)

    # 4. Stemming
    words = stemming(words)

    return words
