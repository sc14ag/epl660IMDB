from __future__ import print_function

import re

import nltk
import pandas as pd
# A very simple Flask Hello World app for you to get started with...
from flask import Flask
from nltk.stem.snowball import SnowballStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import ElasticIndexing

es = ElasticIndexing.Index()
es.implement()

app = Flask(__name__)

# ensures that only the first 100 are read in
titles = es.clustTitles

synopses_wiki = es.clustSynopses
genres = es.clustGenres
ranks = es.clustRanks

print(str(len(titles)) + ' titles')
print(str(len(synopses_wiki)) + ' synopses')
print(str(len(genres)) + ' genres')

# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')

# load nltk's SnowballStemmer as variabled 'stemmer'
stemmer = SnowballStemmer("english")


def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]

    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


totalvocab_stemmed = []
totalvocab_tokenized = []
for i in synopses_wiki:
    allwords_stemmed = tokenize_and_stem(i)
    totalvocab_stemmed.extend(allwords_stemmed)

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)

tfidf_vectorizer = TfidfVectorizer(stop_words='english', use_idf=True, tokenizer=tokenize_and_stem)
tfidf_matrix = tfidf_vectorizer.fit_transform(synopses_wiki)
print(tfidf_vectorizer.get_feature_names())


terms = tfidf_vectorizer.get_feature_names()
dist = 1 - cosine_similarity(tfidf_matrix)


num_clusters = 6
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

films = {'title': titles, 'rank': ranks, 'synopsis': synopses_wiki, 'cluster': clusters, 'genre': genres}
frame = pd.DataFrame(films, index=[clusters], columns=['rank', 'title', 'cluster', 'genre'])

print(frame['cluster'].value_counts())
grouped = frame['rank'].groupby(frame['cluster'])

print(grouped.mean())
print("Top terms per cluster:")
print()

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    for ind in order_centroids[i, :(num_clusters + 1)]:
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=',')
    print()
    print()
    print("Cluster %d titles:" % i, end='')
    for title in frame.ix[i]['title'].values.tolist():
        print(' %s,' % title, end='')
    print()
    print()

if __name__ == '__main__':
    app.run(debug=True)
