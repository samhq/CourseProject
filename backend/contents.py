from utilities import tokenize_str
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


def final_content(url):
    text_content = crawl(url)
    tokenize_content = tokenize_str(text_content)
    
    return " ".join(tokenize_content)
