from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re
import pymorphy3

def prepare_text(text):
    morph = pymorphy3.MorphAnalyzer()
    cleaned_string = re.sub(r'[^А-Яа-яЁё\s.,!?]', '', text)
    cleaned_string = re.sub(r'\.\.+', '', cleaned_string)
    cleaned_string = re.sub(r'  +', '', cleaned_string)
    tokens = [morph.parse(word)[0].normal_form.lower().replace('ё', 'е') for word in cleaned_string.split()]
    return ' '.join(tokens)

def KNN_req(req_corp):

    pairs = [(i, prepare_text(i)) for i in req_corp]

    texts = [pair[1] for pair in pairs]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    k = 5  # Количество кластеров
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(X)

    clusters = [[] for _ in range(k)]  # Создание пустых списков для каждого кластера

    for i, pair in enumerate(pairs):
        cluster_label = kmeans.labels_[i]
        clusters[cluster_label].append(pair[0])

    for cluster_label, cluster in enumerate(clusters):
        print(f"Кластер {cluster_label} : {cluster}")

    return clusters