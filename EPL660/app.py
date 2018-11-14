from flask import render_template
from elasticsearch import Elasticsearch
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    client = Elasticsearch()
    # mapping = '''
    #                      {
    #                       "mappings": {
    #              "movie": {
    #               "properties": {
    #                  "Rank": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Title": {
    #                   "type": "text",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "analyzer" : "fulltext_analyzer"
    #                  },
    #                  "Genre": {
    #                   "type": "text",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Description": {
    #                   "type": "text",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Director": {
    #                   "type": "text",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Actors": {
    #                   "type": "text",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Year": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Runtime(Minutes)": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Rating": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Votes": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Revenue (Millions)": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   },
    #                   "Metascore": {
    #                   "type": "integer",
    #                   "term_vector": "with_positions_offsets_payloads",
    #                   "store" : true,
    #                   "analyzer" : "fulltext_analyzer",
    #                   }

    #               }
    #              },
    #               "settings" : {
    #              "index" : {
    #               "number_of_shards" : 1,
    #               "number_of_replicas" : 0
    #              },
    #               "analysis": {
    #               "analyzer": {
    #                  "fulltext_analyzer": {
    #                   "type": "custom",
    #                   "tokenizer": "whitespace",
    #                   "filter": [
    #                      "lowercase",
    #                      "type_as_payload"
    #                   ]
    #                  }
    #                  }
    #              }
    #           }
    #          }
    #                      }'''
    # client.indices.create(index="test", ignore=400, body=mapping)

    return render_template('userInterface.html')


if __name__ == '__main__':
    app.run()
