from rank_bm25 import BM25Okapi
from contents import *
from utilities import *


def search_query(query, user_id, top_n):
    bookmark_contents = fetch_contents(user_id)
    tokenized_query = remove_stop_words_and_tokenize(
        remove_special_characters(query))
    bm25 = BM25Okapi(bookmark_contents)
    top_results = bm25.get_top_n(tokenized_query, tokenized_query, n=top_n)

    # TODO: top_results need to have the indices from bookmark_contents, 
    # so that we can return the corresponding urls from bookmarks file

    return fetch_bookmarks(user_id, top_results)

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
