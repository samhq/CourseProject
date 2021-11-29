import re
import nltk
from gensim.parsing.preprocessing import remove_stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')


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


def remove_multiple_spaces(text):
    return re.sub('\s+', ' ', text).strip()


def tokenize_str(text):
    # 1. Removing multiple spaces
    text = remove_multiple_spaces(text.lower())

    # 2. Removing stop words
    text = remove_stopwords(text)

    # 3. Tokenization
    words = word_tokenize(text)

    # 4. Removing special characters
    words = remove_special_characters(words)

    # 5. Stemming
    words = stemming(words)
    
    words = list(filter(None, words))

    return words
