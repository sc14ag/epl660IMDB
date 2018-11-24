from flask import Flask
from flask import render_template, request

import ElasticIndexing
from clustering import Clustering

es = ElasticIndexing.Index()
es.implement()
clust= Clustering(es)
app = Flask(__name__)
results = []


@app.route('/')
def hello_world():
    return render_template('userInterface.html',queryResultsFlask="empty")


@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/searchQuery', methods=['POST'])
def query():
    userquery = request.form['userQuery']
    results = es.searchByQuery(userquery)
    # print(results[0][0])
    # similarMovies = clust.findSimilarMovies(results[0][0])
    # print(similarMovies)
    return render_template('userInterface.html', queryResultsFlask=results[0],queryResultsPlot =results[1])


@app.route('/searchCategory', methods=['GET', 'POST'])
def searchCategory():
    category = request.args.get('type')
    categoryResults = es.searchCategory(category)
    print(categoryResults[1])
    return render_template('categorySearch.html',searchCategory=categoryResults[0],searchDes =categoryResults[1] )

@app.route('/view/', methods=['GET'])
def view():
    print('view Details')

    similarUrls = []
    titleMovie =request.args.get('movie')
    similarMovies = clust.findSimilarMovies(titleMovie)
    print(similarMovies)

    movieDetails = es.searchByTitle(titleMovie)
    movieDetailsTitle = movieDetails[0]['Title']
    movieDetailsGenre = movieDetails[0]['Genre']
    movieDetailsDes = movieDetails[0]['Description']
    movieDetailsDir = movieDetails[0]['Director']
    movieDetailsAct = movieDetails[0]['Actors']
    movieDetailsYear = movieDetails[0]['Year']
    movieDetailsMin = movieDetails[0]['Runtime(Minutes)']
    movieDetailRat = movieDetails[0]['Rating']
    movieDetailImg = movieDetails[0]['ImageURL']

    for title in similarMovies:
       similarUrls.append(es.searchByTitle(title)[0]['ImageURL'])
    print(similarUrls)
    return render_template('movieDetails.html',movieTitle =movieDetailsTitle,movieGenre = movieDetailsGenre,moviePlot = movieDetailsDes,movieDir = movieDetailsDir,movieAct=movieDetailsAct,movieYear = movieDetailsYear,
                           movieDur=movieDetailsMin,movieRating=movieDetailRat,simMovies = similarUrls,movieImg = movieDetailImg)

if __name__ == '__main__':
    app.run(debug=True)
