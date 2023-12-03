from giga_util.ClasterTest import get_clarifying_requests
from giga_util.SummarizeTest import prepare_search_results, search_sum
from ml.search import search
import pprint as pp


def split_text(text: str, max_chars: int = 4096) -> list:
    result = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    return result

def telegram_prepare(patents_info, clarified_req):
    final= ''
    for i in patents_info:
        final += '\n' + "<b>PATENT TITLE : " + i[0] + '</b>\n' + '\n'
        final += '\n' + "<a>Ссылка : " + i[1]+ '</a>\n' + '\n'

    final += '\n' + 'Возможные запросы' + '\n'
    for i in clarified_req:
        final += '\n' + i[0] + '\n'

    final = final.\
        replace("</s>", "").replace("<s>", "").replace("</unk>", "").replace("<unk>", "").\
            replace("</n>", "").replace("<n>", "").replace("</p>", "").replace("<p>", "")
    return split_text(final)

def Egor(req , p_g_date_range = '20000101', p_l_date_range = '20100101', p_country = 'RU', limit = 30):

    js_patents = search(req , p_g_date_range, p_l_date_range, p_country , limit)

    clarified_req = get_clarifying_requests(js_patents)

    prepared_patents = prepare_search_results(js_patents)

    search_sum(prepared_patents)

    sums = []

    for patent in prepared_patents:
            sums.append([patent['summary'] ,patent['url'] ])

    return  telegram_prepare(sums, clarified_req)

if __name__ == '__main__':
    s , r = Egor('Ракета', '20000101','20100101','RU', 10)
    pp.pprint(r)
    pp.pprint(s)