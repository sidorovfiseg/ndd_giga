import json

from ml.preprocess import *


from ml import model_embedding

def get_patent_all_keys(dictionary, depth = 0):
    # Получение иерархической структуры патента
    keys = []
    indent = '  ' * depth
    for key, value in dictionary.items():
        keys.append(f"{indent}{key}")
        if isinstance(value, dict):
            nested_keys = get_patent_all_keys(value, depth=depth + 1)
            keys.extend(nested_keys)
    return  json.dumps(keys, indent=2)

def get_patent_url(patent):
    # Получение ссылки на патент из словаря
    tail = '{}{}{}_{}'.format(patent['common']['publishing_office'] , patent['common']['document_number'], patent['common']['kind'], patent['common']['publication_date'].replace('.', ''))
    base = 'https://searchplatform.rospatent.gov.ru/doc/'
    return base + tail

def get_patent_search_url(patent):
    # Получение ссылки на патент для поискового запроса
    tail = '{}{}{}_{}'.format(patent['common']['publishing_office'] , patent['common']['document_number'], patent['common']['kind'], patent['common']['publication_date'].replace('.', ''))
    base = 'https://searchplatform.rospatent.gov.ru/patsearch/v0.2/docs/'
    return base + tail

def get_patent_description(patent):
    return patent['snippet']['description']

def embed_description(patent):
    text = get_patent_description(patent)
    sentences = split_sentences(text)
    # кортеж ебануть
    patent['snippet']['embed_description'] = [model_embedding.encode(i) for i in sentences]