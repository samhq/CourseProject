from rank_bm25 import *
from contents import *
from utilities import *

class IndexBM25Okapi(BM25Okapi):
    def get_top_n_with_indice(self, query, documents, n=5):
        assert self.corpus_size == len(documents), "The documents given don't match the index corpus!"

        scores = self.get_scores(query)
        # print(query, scores)
        top_n = np.argsort(scores)[::-1][:n]
        return top_n

def search_query(query, user_id, top_n, use_keyword_filter=True):
    tokenized_query = preprocess_document_or_query(query)

    if use_keyword_filter:
        query_terms = tokenized_query.split()
        bookmark_contents = [ fetch_contents(user_id)[i] for i in fetch_candidates_docids(user_id, query_terms) ]
    else:
        bookmark_contents = fetch_contents(user_id)

    BM25Okapi = IndexBM25Okapi
    bm25 = BM25Okapi(bookmark_contents)
    top_results = bm25.get_top_n_with_indice(tokenized_query, bookmark_contents, n=top_n)
    # print(top_results)

    return fetch_bookmarks(user_id, top_results)

# if __name__ == '__main__':
#     user_id = "id_1"
#     msg1 = indexPage("https://realpython.com/beautiful-soup-web-scraper-python/", user_id)
#     msg2 = indexPage("https://stackoverflow.com/questions/4690600/python-exception-message-capturing", user_id)
#     msg3 = indexPage("http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm", user_id)
#     msg4 = indexPage("https://dictionarylist.com/en-ur/traceback/", user_id)
#     msg5 = indexPage("https://open.cs.uwaterloo.ca/python-from-scratch/7/7/transcript", user_id)
#     msg6 = indexPage("https://renkun.me/2020/03/31/a-simple-way-to-show-stack-trace-on-error-in-r/", user_id)
#     query = 'tracebackdef blog'
#
#     n = 2
#     use_keyword_filter = True
#     top_n = search_query(query, user_id, n, use_keyword_filter)
#     print(top_n)
