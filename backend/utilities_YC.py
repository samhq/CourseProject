import re
import json
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
import nltk

stemmer = nltk.stem.snowball.EnglishStemmer()

def remove_special_characters(text):
    return re.sub('[^a-zA-Z0-9 ]', '', text)

def remove_stop_words_and_tokenize(text):
    return remove_stopwords(text.lower())

def stem_document_or_query(target):
    target_list = target.split()
    stemmed_list = [stemmer.stem(w) for w in target_list]
    stemmed_str = ' '.join(stemmed_list)
    return stemmed_str

def preprocess_document_or_query(target):
    target = remove_stop_words_and_tokenize(
        remove_special_characters(target))
    return stem_document_or_query(target)


def create_inverted_index_from_corpus(corpus):
    inverted_index = {}
    for docid, document in enumerate(corpus):
        inverted_index = add_document_into_inverted_index(docid, document, inverted_index)
    return inverted_index


def add_document_into_inverted_index(docid, document, inverted_index):
    words = document.split()
    words_distinct = list(set(words))
    for w in words_distinct:
        if w not in inverted_index:
            inverted_index[w] = []
            inverted_index[w].append(docid)
        else:
            inverted_index[w].append(docid)
    return inverted_index

if __name__ == '__main__':
    corpus = ["data mining test she her you he is me are analysis data mining text information her me",
           "tranformers her she me them it is avengers movie blockbuster pirates of the carribean toy story yes",
           "elon musk tesla paypal space electric vehicle her me you the mining"]
    processed_corpus = [preprocess_document_or_query(c) for c in corpus]
    invertedIndex = create_inverted_index_from_corpus(processed_corpus)
    with open('try.json', 'w') as fp:
        json.dump(invertedIndex, fp)

    with open('try.json', 'r') as fp:
        data = json.load(fp)
    print(data['data'])