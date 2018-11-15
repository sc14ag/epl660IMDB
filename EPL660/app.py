from flask import render_template, request
import ElasticIndexing
# A very simple Flask Hello World app for you to get started with...
from flask import Flask


es = ElasticIndexing.Index()
# es.implement()
app = Flask(__name__)


@app.route('/')
def hello_world():

    return render_template('userInterface.html',value= "empty")


@app.route('/searchQuery', methods=['POST'])
def query():

    userquery = request.form['access_token']
    results = es.searchQuery(userquery)
    print (results)
    return render_template('userInterface.html',value = "results")


if __name__ == '__main__':
    app.run(debug=True)
