from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models.gigachat import GigaChat
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents.base import Document
from langchain_core.prompts import PromptTemplate

import pprint as pp
from collections import namedtuple

from ml.patent_utils import get_patent_search_url
from ml.search import search
from ml.parse import get_response_patent, get_format_patent, prepare_patent


giga = GigaChat(credentials = 'NzNkMDNjNDQtOWI3OS00MTI0LWEyOWUtZWYzNmY0YzQxYzM1OjIxYTFhNjU3LTBkODAtNGVkNS1hODJkLTE4MmRjNjU1NWNjMg==', verify_ssl_certs = False)

def split_string(string, chunk_size):
    return [string[i : i + chunk_size] for i in range(0, len(string), chunk_size)]

def seak_and_destroy(req , p_g_date_range, p_l_date_range, p_country, limit = 5):
    res = []
    js_patents = search(req , p_g_date_range , p_l_date_range , p_country , limit)

    patents = []

    for p in js_patents['hits']:

        #TODO Класстеризация

        n = get_patent_search_url(p)
        t = get_response_patent(n)
        patents.append(t)

    for patent in patents:
        p = get_format_patent(patent)
        pp.pprint(p)
        p['text'] = prepare_patent(p['text'])
        res.append(p)
    return res

patents = seak_and_destroy('Ракета', '20000101', '20100101', 'RU', 5)

print(patents[0])

def sum_patent(patent):
    DOC = namedtuple('DOC', ['page_content', 'metadata', 'type'])
    text = ''
    for i in patent['text'].keys():
        text += patent['text'][i]

    print(len(text))

    chunks = split_string(text, 5000)

    docs = [DOC(i, {}, 'Document') for i in chunks ]

    chain = load_summarize_chain(llm=giga, chain_type="map_reduce")

    res = chain.run(docs)

    return res


def search_sum(patents):
    for p in patents:
        sum_p = sum_patent(p)
        p.update({'summary' : sum_p})


def Egor(req , p_g_date_range, p_l_date_range, p_country, limit = 5):
    patents = seak_and_destroy(req, p_g_date_range, p_l_date_range, p_country, limit)
    search_sum(patents)
    return patents

'''



print("\n\n===")
pp.pprint(res)
print('965_123')

'''
