

import json
import re
import requests
import pprint as pp

base = 'https://searchplatform.rospatent.gov.ru/patsearch/v0.2/docs/'
tail = 'CN0202122833U_20120125'
url = base + tail

def get_response_patent(url):
    # Получение конкретного патента в виде словаря
    token = "f0048ed764374ae2897424fd7ad6074d"

    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    data_row = {'limit': 10, 'filter': {'date_published': {'range': {'gt': '20000101', 'lt': '20010101'}}}}

    # response = requests.post(url, headers = headers, data= json.dumps(data_row))
    response = requests.post(url, headers=headers, data=json.dumps(data_row))

    print(response.status_code)

    return json.loads(response.text)

t = get_response_patent(url)
pp.pprint(t)