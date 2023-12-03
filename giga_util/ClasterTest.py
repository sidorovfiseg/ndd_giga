from langchain.schema import HumanMessage, SystemMessage

import pprint as pp
from giga_util.KNN import KNN_req
from giga_util import chat


def feature_extraction(text):
    # очистить текст
    messages = [
        SystemMessage(
            content="Перед тобой технический текс. Придумай к нему технический заголовок отражающий его суть."
        )
    ]
    messages.append(HumanMessage(content=text))
    res = chat(messages)
    messages.append(res)

    return res.content # Признаки патента str

def get_patent_clastering(js_patents ):
    # Выделение ключевых слов
    feature_set = []

    for n, p in enumerate(js_patents['hits']):
        f = feature_extraction(p['snippet']['description'])
        feature_set.append(f)
    return feature_set

def clarifying(reqs):

    text = ', '.join(reqs)
    messages = [
        SystemMessage(
            content = "Дан примеры запросов к базе данных через запятую. Пожалуйста, выдели тематику в одном предложении."
        )
    ]
    messages.append(HumanMessage(content=text))
    res = chat(messages)
    messages.append(res)

    return res.content

def get_clarifying_requests(js_patents):
    res = []
    req_corp = get_patent_clastering(js_patents)

    total = len(req_corp)

    clasters = KNN_req(req_corp)

    for i in clasters:
        curent = len(i)
        clarified_req = clarifying(i)
        procent = round(curent / total * 100)
        res.append([clarified_req, procent])
    return res


