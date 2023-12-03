from langchain.chains.summarize import load_summarize_chain
import pprint as pp
from collections import namedtuple

from ml.patent_utils import get_patent_search_url
from ml.parse import get_response_patent, get_format_patent, prepare_patent
from giga_util import chat

def split_string(string, chunk_size):
    return [string[i : i + chunk_size] for i in range(0, len(string), chunk_size)]

def prepare_search_results(js_patents):
    res = []
    # Подготовка к суммаризации
    for p in js_patents['hits'][:3]:
        n = get_patent_search_url(p) # получение ссылки на патент
        t = get_response_patent(n)   # js патент
        p = get_format_patent(t)     # Перевод патента в нужный формат
        p['text'] = prepare_patent(p['text']) # очистка
        res.append(p)
    return res
def sum_patent(patent):
    DOC = namedtuple('DOC', ['page_content', 'metadata', 'type'])
    text = ''

    for i in patent['text'].keys():
        text += patent['text'][i]

    print(len(text))
    chunks = split_string(text, 5000)[:3]
    docs = [DOC(i, {}, 'Document') for i in chunks ]
    chain = load_summarize_chain(llm = chat, chain_type="map_reduce")
    res = chain.run(docs)
    return res
def search_sum(prepared_patents):
    for p in prepared_patents:
        sum_p = sum_patent(p)
        p.update({'summary' : sum_p})


