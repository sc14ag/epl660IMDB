import flask
from flask import render_template, request
import ElasticIndexing
# A very simple Flask Hello World app for you to get started with...
from flask import Flask

es = ElasticIndexing.Index()
# es.implement()
app = Flask(__name__)
results = []


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('userInterface.html',queryResultsFlask="empty")


@app.route('/searchQuery', methods=['POST'])
def query():
    userquery = request.form['userQuery']
    results = es.searchQuery(userquery)
    return render_template('userInterface.html', queryResultsFlask=results[0],queryResultsPlot =results[1])


if __name__ == '__main__':
    app.run(debug=True)
