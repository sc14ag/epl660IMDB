from __future__ import print_function
from elasticsearch import Elasticsearch


class Index:
    """
    This class indexes files in a given path,passed as a parameter
    """

    def __init__(self):
        self.client = None
        self.counter = 0
        self.client = Elasticsearch()
        self.lineElements =[]
        self.titles = []
        self.synopses = []


        # mapping = '''
        #                  {
        #                   "mappings": {
        #          "movie": {
        #           "properties": {
        #              "Rank": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Title": {
        #               "type": "text",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "analyzer" : "fulltext_analyzer"
        #              },
        #              "Genre": {
        #               "type": "text",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Description": {
        #               "type": "text",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Director": {
        #               "type": "text",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Actors": {
        #               "type": "text",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Year": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Runtime(Minutes)": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Rating": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Votes": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Revenue (Millions)": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               },
        #               "Metascore": {
        #               "type": "integer",
        #               "term_vector": "with_positions_offsets_payloads",
        #               "store" : true,
        #               "analyzer" : "fulltext_analyzer",
        #               }
        #
        #           }
        #          },
        #           "settings" : {
        #          "index" : {
        #           "number_of_shards" : 1,
        #           "number_of_replicas" : 0
        #          },
        #           "analysis": {
        #           "analyzer": {
        #              "fulltext_analyzer": {
        #               "type": "custom",
        #               "tokenizer": "whitespace",
        #               "filter": [
        #                  "lowercase",
        #                  "type_as_payload"
        #               ]
        #              }
        #              }
        #          }
        #       }
        #      }
        #                  }'''
        # self.client.indices.create(index="imdb", ignore=400, body=mapping)
    def implement(self):
        
        print ("mpika")
        f = open('static/IMDB-Movie-Data.csv', 'r')
        lines = f.readlines()[1:]
        for line in lines:
            self.lineElements = line.split(',')

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
                "Metascore": self.lineElements[11].replace("\n","")
            }

            self.client.index(index="imdb", doc_type='movie', id=(int(self.lineElements[0])-1), body=json)
        f.close()

    def searchCategory(self,category):
        res = self.client.search(index="imdb", doc_type="movie", body={"query": {"match": {"Genre": category}}})
        print("%d documents found" % res['hits']['total'])
        for doc in res['hits']['hits']:
            print("%s) %s" % (doc['_id'], doc['_source']['Title']))

    def searchQuery (self,userQuery):
        results= []
        res = self.client.search(index="imdb4", doc_type="movie", body={"query": {"multi_match": {"query": userQuery}}})
        print("%d documents found" % res['hits']['total'])
        for doc in res['hits']['hits']:
            results.append(doc["_source"]['Title'])

        return results