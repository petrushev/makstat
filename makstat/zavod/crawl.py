from requests import get
from lxml.html import fromstring


BASE_URL = 'http://makstat.stat.gov.mk/pxweb2007bazi/Database'
TREE = BASE_URL + '/StatistikaPoOblasti/databasetreeNodes.js'

def categories():
    """Returns dictinary of available categories as keys
    and their urls as values """
    rq = get(TREE)
    doc = rq.content.decode('cp1251')
    categories_ = {}
    for line in doc.split('\r\n'):
        if not line.startswith('insDoc'):
            continue
        text, link = line.split('gLnk(')[1].rstrip(')').split(',')[1:]
        text = text.strip('"')
        link = BASE_URL + link.strip('"')[2:]
        categories_[text] = link
    return categories_

def docs_in_category(url):
    """Returns dictionary of avaliable documents for given category url
    The keys are the name of the document and the links are the values"""
    rq = get(url)
    doc = fromstring(rq.content.decode('cp1251'))
    doc.make_links_absolute(url)

    docs = {}

    for item in doc.cssselect('li'):
        title = item.cssselect('b')
        if len(title) == 0:
            continue
        title = title[0].text_content()
        for a in item.cssselect('a[href]'):
            href = a.attrib['href']
            if not href.endswith('.px'):
                continue
            docs[title] = href

    return docs
