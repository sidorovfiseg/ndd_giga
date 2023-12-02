import json
import requests
import pprint as pp
def search(req , p_g_date_range= '20000101', p_l_date_range='20100101', p_country = 'RU', limit = 10):
    # Функция поиска корпуса патентов по заданным критериям

    token = "f0048ed764374ae2897424fd7ad6074d"
    url = "https://searchplatform.rospatent.gov.ru/patsearch/v0.2/search"

    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}

    filter = {"country": {"values": [p_country]}, 'date_published': {'range': {'gt': p_g_date_range, 'lt' : p_l_date_range }}}
    #pp.pprint(filter)
    data_row = {'q' : req , 'limit': limit, 'filter': filter}

    # response = requests.post(url, headers = headers, data= json.dumps(data_row))
    response = requests.post(url, headers=headers, data=json.dumps(data_row))

    #print(response.status_code)
    #print(response.text)
    return json.loads(response.text)

if __name__ == '__main__':
    t = search('Ракета')
    print(t['total'])



