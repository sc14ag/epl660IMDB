from __future__ import print_function
from elasticsearch import Elasticsearch
import io


class Index:
    """
    This class indexes files in a given path,passed as a parameter
    """

    def __init__(self):
        self.client = None
        self.counter = 0
        self.client = Elasticsearch()
        self.lineElements =[]
        self.clustTitles = []
        self.clustGenres = []
        self.clustRanks = []
        self.titles = []
        self.clustSynopses =[]


    def implement(self):
        f = io.open('static/IMDB-Movie-Data.csv',encoding='utf8')
        lines = f.readlines()[1:]
        for line in lines:
            self.lineElements = line.split(',')
            self.clustTitles.append(self.lineElements[1].replace("\n","").replace("\n",""))
            self.clustSynopses.append(str(self.lineElements[3].replace("_",",").replace("\n","")))
            self.clustGenres.append(self.lineElements[2].replace("_",",").replace("\n",""))
            self.clustRanks.append(int(self.lineElements[0].replace("\n","")))
            json = {

                "Rank": self.lineElements[0].replace("\n",""),
                "Title": self.lineElements[1].replace("_",",").replace("\n",""),
                "Genre": self.lineElements[2].replace("_",",").replace("\n",""),
                "Description": self.lineElements[3].replace("_",",").replace("\n",""),
                "Director": self.lineElements[4].replace("\n",""),
                "Actors": self.lineElements[5].replace("_",",").replace("\n",""),
                "Year": self.lineElements[6].replace("\n",""),
                "Runtime(Minutes)": self.lineElements[7].replace("\n",""),
                "Rating": self.lineElements[8].replace("\n",""),
                "Votes": self.lineElements[9].replace("\n",""),
                "Revenue(Millions)": self.lineElements[10].replace("\n",""),
                "Metascore": self.lineElements[11].replace("\n",""),
                "ImageURL":self.lineElements[12].replace("\n","").replace("\"","")
            }

            self.client.index(index="imdb", doc_type='movie', id=(int(self.lineElements[0])-1), body=json)
        f.close()

    def searchCategory(self,category):

        resultsDes = []
        res = self.client.search(index="imdb", doc_type="movie", body={"query": {"match": {"Genre": category}}})
        for doc in res['hits']['hits']:
            resultsDes.append(doc['_source'])
        return resultsDes

    def searchByQuery (self,userQuery):
        results= []
        resultsPlot = []
        res = self.client.search(index="imdb", doc_type="movie", body={"query": {"multi_match": {"query": userQuery, "fields":[ "Title", "Description" ]}}})
        print("%d documents found" % res['hits']['total'])
        for doc in res['hits']['hits']:
            results.append(doc["_source"]['Title'])
            resultsPlot.append(doc["_source"]['Description'])
        return results, resultsPlot

    def searchByTitle (self,title):
        resultsDetails = []
        res = self.client.search(index="imdb", doc_type="movie", body={"query": {"match": {"Title": title}}})
        print("%d documents found" % res['hits']['total'])
        for doc in res['hits']['hits']:
            resultsDetails.append(doc['_source'])
        return resultsDetails




