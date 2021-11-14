from utilities import *
import requests
from bs4 import BeautifulSoup


def crawl(page_url):
    # given a website url, crawl that page, extract text
    # return the text

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

    # print(output)
    return output


def indexPage(page_url, user_id):
    # for simplicity, assume that there is a folder named `user_id` in your system
    # - remove the stop words from the text
    # - add the text in a file name `contents` and add the url to a file name `bookmarks`
    # - make an inverted index and save in the user's folder

    msg = ""
    err = False

    try:
        bookmark_file = user_id + "/bookmark.txt"
        content_file = user_id + "/contents.txt"

        # first, check if the user already bookmarked this page
        # read the contents of `bookmark_file` in a list
        # check if `page_url` exists or not
        # if exists, then just return (do nothing)
        # else, execute the remaining statements

        # TODO: checking the url's presence

        # get page content
        page_content = crawl(page_url)

        # TODO: append the tokenized_content in `content_file`
        tokenized_content = remove_stop_words_and_tokenize(
            remove_special_characters(page_content))

        # TODO: append the url in `bookmark_file`

    except:
        # TODO: exception occurred, set the error
        msg = "error"
        err = True
    else:
        msg = "success"
        err = False
    finally:
        # close any opened file
        pass

    return msg


def fetch_contents(user_id):
    # TODO: Add function to fetch bookmark contents given a specific user
    contents = []

    return contents


def fetch_bookmarks(user_id, indices):
    # TODO: fetch the list of urls (or maybe dict for urls and names)
    urls = []

    return urls
