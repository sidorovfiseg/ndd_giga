import nltk
import requests
import json
import keyboard

import pprint as pp
import pickle

def get_all_keys(dictionary, depth=0):
    keys = []
    indent = '    ' * depth
    for key, value in dictionary.items():
        keys.append(f"{indent}{key}")
        if isinstance(value, dict):
            nested_keys = get_all_keys(value, depth=depth + 1)
            keys.extend(nested_keys)
    return keys


def get_response_text():
    token = "f0048ed764374ae2897424fd7ad6074d"
    url = "https://searchplatform.rospatent.gov.ru/patsearch/v0.2/search"

    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    data_row = {'limit': 10, 'filter': {'date_published': {'range': {'gt': '20000101'}}}}

    # response = requests.post(url, headers = headers, data= json.dumps(data_row))

    print(json.dumps(data_row))
    response = requests.post(url, headers=headers, data=json.dumps(data_row))

    print(response.status_code)
    print(response.text)

    return json.loads(response.text)

a = get_response_text()
print(a)

'''
pp.pprint(patent)

all_keys = get_all_keys(patent)
json_str = json.dumps(all_keys, indent=2)
print(json_str)
'''