from __future__ import print_function

import random
import re

import nltk
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# import ElasticIndexing
#
# es = ElasticIndexing.Index()
# es.implement()

#
# ensures that only the first 100 are read in
class Clustering:

    def __init__(self,es):
        self.titles = es.clustTitles
        self.synopses_wiki = es.clustSynopses
        self.genres = es.clustGenres
        self.ranks = es.clustRanks

        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stemmer = SnowballStemmer("english")
        self.num_clusters = 6

        totalvocab_stemmed = []
        totalvocab_tokenized = []
        for i in self.synopses_wiki:
            allwords_stemmed = self.tokenize_and_stem(i)
            totalvocab_stemmed.extend(allwords_stemmed)

            allwords_tokenized = self.tokenize_only(i)
            totalvocab_tokenized.extend(allwords_tokenized)

        self.vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)

        tfidf_vectorizer = TfidfVectorizer(stop_words='english', use_idf=True, tokenizer=self.tokenize_and_stem)
        tfidf_matrix = tfidf_vectorizer.fit_transform(self.synopses_wiki)
        print(tfidf_vectorizer.get_feature_names())

        self.terms = tfidf_vectorizer.get_feature_names()
        dist = 1 - cosine_similarity(tfidf_matrix)


        km = KMeans(n_clusters=self.num_clusters)
        km.fit(tfidf_matrix)
        self.clusters = km.labels_.tolist()

        films = {'title': self.titles, 'rank': self.ranks, 'synopsis': self.synopses_wiki, 'cluster': self.clusters,
                 'genre': self.genres}
        self.frame = pd.DataFrame(films, index=[self.clusters], columns=['rank', 'title', 'cluster', 'genre'])


        grouped = self.frame['rank'].groupby(self.frame['cluster'])



        self.order_centroids = km.cluster_centers_.argsort()[:, ::-1]

        for i in range(self.num_clusters):
            print("Cluster %d words:" % i, end='')
            for ind in self.order_centroids[i, :(self.num_clusters + 1)]:
                print(' %s' % self.vocab_frame.ix[self.terms[ind].split(' ')].values.tolist()[0][0], end=',')
            print()
            print()
            print("Cluster %d titles:" % i, end='')
            for title in self.frame.ix[i]['title'].values.tolist():
                print(' %s,' % title, end='')
            print()
            print()

    def findSimilarMovies(self,query_result):

            for i in range(self.num_clusters):
                    if query_result in self.frame.ix[i]['title'].values.tolist():
                        return (random.sample(self.frame.ix[i]['title'].values.tolist(), 3))


    def tokenize_and_stem(self,text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [self.stemmer.stem(t) for t in filtered_tokens]

        return stems


    def tokenize_only(self,text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        return filtered_tokens