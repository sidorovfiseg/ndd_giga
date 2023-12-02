import json
import re
import requests
import pprint as pp

def get_response_patent(url):
    # Получение конкретного патента в виде словаря
    token = "f0048ed764374ae2897424fd7ad6074d"

    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    data_row = {'limit': 10, 'filter': {'date_published': {'range': {'gt': '20000101', 'lt': '20010101'}}}}

    # response = requests.post(url, headers = headers, data= json.dumps(data_row))
    response = requests.post(url, headers=headers, data=json.dumps(data_row))

    print(response.status_code)

    return json.loads(response.text)


def prepare_text(text):
    cleaned_string = re.sub(r'[^А-Яа-яЁё\s.,!?]', '', text)
    cleaned_string = re.sub(r'\.\.+', '', cleaned_string)
    cleaned_string = re.sub(r'  +', '', cleaned_string)
    return cleaned_string

def get_format_patent(data):
    # Получаем словарь представляющий собой текст патента по главам
    abstract = next(iter(data['abstract'].values()))
    claims = next(iter(data['claims'].values()))
    description = next(iter(data['description'].values()))
    mpk = data['common']['classification']
    url = 'https://searchplatform.rospatent.gov.ru/doc/' + data['id']
    return    {'text' : {'abstract' : abstract, 'claims' : claims, 'description' : description}, 'mpk' : mpk, 'url' : url}

def prepare_patent(patent):
    text = patent
    for key in text.keys():
        text[key] = prepare_text(text[key])
    return text

'''
if __name__ == '__main__':
    text = get_response_text()
    print(len(text['hits']))
    text = get_text(text)

    text = prepare_patent(text)

    pp.pprint(text)
'''

