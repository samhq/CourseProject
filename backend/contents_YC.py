import os
import json
import traceback

from utilities import *
import requests
from bs4 import BeautifulSoup
import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer

BOOKMARKS_FNAME = '/bookmarks.txt'
CONTENTS_FNAME = '/contents.txt'
INVERTED_INDEX_FNAME = '/inverted_index.json'

def crawl(page_url):
    # given a website url, crawl that page, extract text
    # return the text
    # TODO: how to crawl the website that requires log in(e.g. https://medium.com/swlh/demystifying-a-web-search-problem-using-inverted-index-c6df8236291)

    res = requests.get(page_url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script'
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return output

def user_exits(user_id):
    return os.path.exists(user_id)

def init_user_create_files(user_id):
    os.mkdir(user_id)
    with open(user_id + BOOKMARKS_FNAME, 'w'): pass
    with open(user_id + CONTENTS_FNAME, 'w'): pass
    with open(user_id + INVERTED_INDEX_FNAME, 'w') as fp:
        json.dump({}, fp)


def url_in_bookmarks(url, bookmarks_path):
    with open(bookmarks_path, "r") as bookmarks_file:
        lines = bookmarks_file.read().splitlines()
        return url in lines

def append_newline_to_file(newline, file_path):
    with open(file_path, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(newline)

def indexPage(page_url, user_id):
    msg = ""
    err = False

    try:
        bookmarks_path = user_id + BOOKMARKS_FNAME
        contents_path = user_id + CONTENTS_FNAME
        inverted_index_path = user_id + INVERTED_INDEX_FNAME

        if user_exits(user_id) == False:
            init_user_create_files(user_id)

        # checking the url's presence
        if url_in_bookmarks(page_url, bookmarks_path):
            msg = "url already exists in bookmarks.txt, do nothing."
            return msg

        # get page content
        page_content = crawl(page_url)

        # append the tokenized_content in `content_file`
        preprocessed_content = preprocess_document_or_query(page_content)
        append_newline_to_file(preprocessed_content, contents_path)

        # append the url in `bookmarks_file`
        append_newline_to_file(page_url, bookmarks_path)

        # add current page into inverted index
        docid = len(fetch_contents(user_id)) - 1
        inverted_index = {}
        with open(inverted_index_path, 'r') as fp:
            inverted_index = json.load(fp)
        add_document_into_inverted_index(docid, preprocessed_content, inverted_index)
        with open(inverted_index_path, 'w') as fp:
            json.dump(inverted_index, fp)

    except Exception as e:
        # exception occurred, set the error
        msg = "Errors in indexPage(" + user_id + ", "+ page_url + ")\n" + str(e)
        print(traceback.format_exc())
        err = True
    else:
        msg = "success"
        err = False
    finally:
        pass

    return msg


def fetch_contents(user_id):
    with open(user_id + CONTENTS_FNAME, 'r') as contents_file:
        contents = contents_file.read().splitlines()

    return contents

def fetch_bookmarks(user_id, indices):
    with open(user_id + BOOKMARKS_FNAME, 'r') as bookmarks_file:
        bookmarks = bookmarks_file.read().splitlines()

    urls = [bookmarks[i] for i in indices]
    return urls

def fetch_candidates_docids(user_id, query_terms):
    # e.g. query_terms = ['hi', 'hello']

    inverted_index_path = user_id + INVERTED_INDEX_FNAME
    inverted_index = {}
    with open(inverted_index_path, 'r') as fp:
        inverted_index = json.load(fp)

    candidates = []
    for word in query_terms:
        if word in inverted_index:
            candidates = candidates + inverted_index[word]

    return list(set(candidates))

if __name__ == '__main__':
    user_id = "id_1"
    #msg1 = indexPage("https://realpython.com/beautiful-soup-web-scraper-python/", user_id)
    #msg2 = indexPage("https://stackoverflow.com/questions/4690600/python-exception-message-capturing", user_id)
    #msg3 = indexPage("http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm", user_id)
    #print(fetch_candidates_docids(user_id, ['tracebackdef', 'blog']))