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

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/categories')
def categories():

    imageAction= es.searchCategory("Action")[0]['ImageURL']
    imageAdventure = es.searchCategory("Adventure")[0]['ImageURL']
    imageAnimation = es.searchCategory("Animation")[0]['ImageURL']
    imageBiography = es.searchCategory("Biography")[0]['ImageURL']
    imageComedy = es.searchCategory("Comedy")[0]['ImageURL']
    imageCrime = es.searchCategory("Crime")[0]['ImageURL']
    imageDrama = es.searchCategory("Drama")[0]['ImageURL']
    imageFamily = es.searchCategory("Family")[0]['ImageURL']
    imageFantasy = es.searchCategory("Fantasy")[0]['ImageURL']

    imageHorror = es.searchCategory("Horror")[0]['ImageURL']
    imageMusic = es.searchCategory("Music")[0]['ImageURL']
    imageMusical = es.searchCategory("Musical")[0]['ImageURL']
    imageMystery = es.searchCategory("Mystery")[0]['ImageURL']
    imageRomance = es.searchCategory("Romance")[0]['ImageURL']
    imageScifi = es.searchCategory("Sci-fi")[0]['ImageURL']
    imageSport = es.searchCategory("Sport")[0]['ImageURL']
    imageThriller = es.searchCategory("Thriller")[0]['ImageURL']
    imageWar = es.searchCategory("War")[0]['ImageURL']
    imageWestern = es.searchCategory("Western")[0]['ImageURL']


    return render_template('categories.html', imgAction= imageAction, imgAdventure=imageAdventure, imgAnimation= imageAnimation, imgBio=imageBiography, imgComdedy= imageComedy,
imgCrime=imageCrime, imgDrama=imageDrama, imgFamily=imageFamily, imgFantasy=imageFantasy, imgHorror= imageHorror, imgMusic=imageMusic,imgMusical=imageMusical,
                           imgMystery= imageMystery, imgRom=imageRomance, imgScifi=imageScifi, imgSport= imageSport, imgThriller= imageThriller, imgWar=imageWar,
                           imgWestern=imageWestern)

@app.route('/searchQuery', methods=['POST'])
def query():
    userquery = request.form['userQuery']
    results = es.searchByQuery(userquery)
    similarMovies = clust.findSimilarMovies(results[0][0])
    return render_template('userInterface.html', queryResultsFlask=results[0],queryResultsPlot =results[1])


@app.route('/searchCategory', methods=['GET', 'POST'])
def searchCategory():
    category = request.args.get('type')
    categoryResults = es.searchCategory(category)
    return render_template('categorySearch.html',searchCategory=categoryResults,searchDes =categoryResults,searchImg = categoryResults,movieCategory=category)

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
