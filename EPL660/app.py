from flask import render_template
from elasticsearch import Elasticsearch
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

def ElasticIndex():
    f = open('static/IMDB-Movie-Data.csv', 'r')
    es = Elasticsearch()
    lines = f.readlines()[1:]
    for line in lines:
        lineElements = line.split(',')

        json = {

                    "Rank": lineElements[0].replace("\n", ""),
                    "Title": lineElements[1].replace("_", ",").replace("\n", ""),
                    "Genre": lineElements[2].replace("_", ",").replace("\n", ""),
                    "Description": lineElements[3].replace("_", ",").replace("\n", ""),
                    "Director": lineElements[4].replace("\n", ""),
                    "Actors": lineElements[5].replace("_", ",").replace("\n", ""),
                    "Year": lineElements[6].replace("\n", ""),
                    "Runtime(Minutes)": lineElements[7].replace("\n", ""),
                    "Rating": lineElements[8].replace("\n", ""),
                    "Votes": lineElements[9].replace("\n", ""),
                    "Revenue(Millions)": lineElements[10].replace("\n", ""),
                    "Metascore": lineElements[11].replace("\n", "")
                }

        es.index(index="epl661", doc_type='movie', id=(int(lineElements[0]) - 1), body=json)

ElasticIndex()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('userInterface.html')


if __name__ == '__main__':
    app.run(debug=True)
