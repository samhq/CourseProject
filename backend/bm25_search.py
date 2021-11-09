import re
from gensim.parsing.preprocessing import STOPWORDS
from rank_bm25 import *


def remove_special_characters(seq):
    return re.sub('[^a-zA-Z0-9 ]', '', seq)


def remove_stop_words_and_tokenize(seq):
    return [word for word in seq.lower().split() if word not in STOPWORDS]


def fetch_bookmark_contents(username):
    # TODO: Add function to fetch bookmark contents given a specific user
    pass


def search_query(query, username, top_n):
    bookmark_contents = fetch_bookmark_contents(username)
    tokenized_contents = [remove_stop_words_and_tokenize(remove_special_characters(content)) for content in bookmark_contents]
    tokenized_query = remove_stop_words_and_tokenize(remove_special_characters(query))
    bm25 = BM25Okapi(tokenized_contents)
    top_results = bm25.get_top_n(tokenized_query, tokenized_contents, n=top_n)
    return top_results

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
