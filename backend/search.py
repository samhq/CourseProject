from rank_bm25 import BM25Okapi
from contents import *
from utilities import *
import numpy as np
import operator


def search_query(query, top_n, corpus):
    tokenized_corpus = [remove_stop_words_and_tokenize(
        remove_special_characters(doc)) for doc in corpus]
    tokenized_query = remove_stop_words_and_tokenize(
        remove_special_characters(query))
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(tokenized_query)
    d = dict()
    for (x,), y in np.ndenumerate(scores):
        if (y > 0):
            d[x] = y

    cd = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    top = dict(cd[:int(top_n)])

    return top

# corpus = ["data mining test she her you he is me are analysis data mining text information her me",
#           "tranformers her she me them it is avengers movie blockbuster pirates of the carribean toy story yes",
#           "elon musk tesla paypal space electric vehicle her me you the mining"]
#
# tokenized_corpus = [remove_stop_words_and_tokenize(remove_special_characters(doc)) for doc in corpus]
# query = "data mining"
# tokenized_query = remove_stop_words_and_tokenize(remove_special_characters(query))
# bm25 = BM25Okapi(tokenized_corpus)
# doc_scores = bm25.get_scores(tokenized_query)
# top_1 = bm25.get_top_n(tokenized_query, corpus, n=1)
# print(doc_scores)
# print(top_1)
