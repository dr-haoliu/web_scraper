from collections import defaultdict
from simplejson import JSONDecodeError
import urllib3

from pyquery import PyQuery as pq
from xml.etree import ElementTree
import backoff
import requests
import time
import datetime
import json



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_pubmed_linked_articles_url(nct_id, completion_date,
                                   query_type):
    url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    url += 'esearch.fcgi?db=pubmed&retmode=json&term='
    url += '(%s[si] OR %s[Title/Abstract]) ' % (nct_id, nct_id)
    url += 'AND ("%s"[pdat] : ' % completion_date.strftime('%Y/%m/%d')
    url += '"3000"[pdat]) '
    if query_type == 'broad':
        url += "AND ((clinical[Title/Abstract] AND trial[Title/Abstract]) "
        url += "OR clinical trials as topic[MeSH Terms] "
        url += "OR clinical trial[Publication Type] "
        url += "OR random*[Title/Abstract] "
        url += "OR random allocation[MeSH Terms] "
        url += "OR therapeutic use[MeSH Subheading])"
    elif query_type == 'narrow':
        url += "AND (randomized controlled trial[Publication Type] OR "
        url += "(randomized[Title/Abstract] "
        url += "AND controlled[Title/Abstract] AND trial[Title/Abstract]))"
    return url


def get_response(url):
    return requests.get(url)

def extract_pubmed_ids_from_json(data):
    ids = []
    esearchresult = data['esearchresult']
    if 'idlist' in esearchresult:
        ids = esearchresult['idlist']
    return ids

def is_study_protocol(title):
    return (title and b'study protocol' in title.lower())

def normalise_phase(x):
    '''
    Set N/A (trials without phases, e.g. device trials) to 5
    (i.e. later than phase 2, which is our cutoff for inclusion).
    And set multi-phase trials to the earlier phase, e.g.
    phase 1/2 trials to 1.
    '''
    mapping = {
        'Early 1': 1,
        '1/2': 1,
        '2/3': 2,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        'N/A': 5
    }
    return mapping[x]


def extract_title_from_pubmed_data(text):
    try:
        tree = ElementTree.fromstring(text)
        title = tree.find('.//Article/ArticleTitle')
        if title is not None and title.text is not None:
            title = title.text.encode('utf8')
        if type(title) != bytes:
            title = ''
    except ElementTree.ParseError:
        print('ParseError', text)
        title = ''
    return title

def get_pubmed_title(pmid):
    '''
    Retrieve the title of a PubMed article, from its PMID.
    '''
    url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    url += 'db=pubmed&rettype=abstract&id=%s' % pmid
    resp = get_response(url)
    title = extract_title_from_pubmed_data(resp.content)
    return title

def get_pubmed_linked_articles(nct_id, completion_date, query_type):
    '''
    Given an NCT ID, search PubMed for related results articles.
    '''
    url = get_pubmed_linked_articles_url(nct_id, completion_date,
                                         query_type)
    resp = get_response(url)
    data = resp.json()
    ids = extract_pubmed_ids_from_json(data)
    for id1 in ids[:]:
        title = get_pubmed_title(id1)
        if is_study_protocol(title):
            ids.remove(id1)
        time.sleep(0.5)
    return ids

def test_get_pubmed_linked_articles_url():
    d = datetime.datetime(2010, 1, 1)
    base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
    base += 'db=pubmed&retmode=json'
    base += '&term=(NCT01020916[si] OR NCT01020916[Title/Abstract]) '
    base += 'AND ("2010/01/01"[pdat] : "3000"[pdat])%s'
    url = get_pubmed_linked_articles_url('NCT01020916', d, '')
    assert url == base % ' '
    url = get_pubmed_linked_articles_url('NCT01020916', d, 'broad')
    s = ' AND ((clinical[Title/Abstract] AND trial[Title/Abstract]) '
    s += 'OR clinical trials as topic[MeSH Terms] OR '
    s += 'clinical trial[Publication Type] OR random*[Title/Abstract] '
    s += 'OR random allocation[MeSH Terms] OR '
    s += 'therapeutic use[MeSH Subheading])'
    assert url == base % s
    url = get_pubmed_linked_articles_url('NCT01020916', d, 'narrow')
    s = ' AND (randomized controlled trial[Publication Type] '
    s += "OR (randomized[Title/Abstract] AND "
    s += "controlled[Title/Abstract] AND trial[Title/Abstract]))"
    assert url == base % s



def test_is_study_protocol():
    r = is_study_protocol('Study protocol: foo')
    assert r
    r = is_study_protocol('Bar foo')
    assert not r


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    d = datetime.datetime(2000, 1, 1)
    print(get_pubmed_linked_articles('NCT01020916', d, 'narrow'))
    print(get_pubmed_linked_articles('NCT03086369', d, 'narrow'))
    print(get_pubmed_linked_articles('NCT00007644', d, 'narrow'))

