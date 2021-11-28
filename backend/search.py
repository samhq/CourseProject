from rank_bm25 import BM25Okapi
from utilities import tokenize_str
import numpy as np
import operator


def search_query(query, top_n, corpus):
    tokenized_corpus = [doc.split(" ") for doc in corpus]
    tokenized_query = tokenize_str(query)
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(tokenized_query)
    d = dict()
    for (x,), y in np.ndenumerate(scores):
        if (y > 0):
            d[x] = y

    cd = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    top = dict(cd[:int(top_n)])

    return top
