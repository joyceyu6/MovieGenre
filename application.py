from flask import (
    Flask, render_template, request, redirect, jsonify, url_for, flash
)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie, User
from flask import session as login_session  # added for login
import random
import string

# added for facebook login
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

APPLICATION_NAME = "Catalog Application"

# Connect to Database and create database session

engine = create_engine('sqlite:///genremovie.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in xrange(32)
    )

    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Facebook login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?' \
          'grant_type=fb_exchange_token&client_id=%s&client_secret=%s&' \
          'fb_exchange_token=%s' \
          % (app_id, app_secret, access_token)

    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?' \
          'access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?' \
          'access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;' \
              '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'

    flash("Now logged in as %s" % login_session['username'])
    return output


# Facebook disconnect
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' \
          % (facebook_id, access_token)

    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


# JSON APIs to view Genre Movie Information
@app.route('/genre/<int:genre_id>/movie/JSON')
def genreMovieJSON(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    return jsonify(Movie=[i.serialize for i in movies])


@app.route('/genre/<int:genre_id>/movie/<int:movie_id>/JSON')
def movieJSON(genre_id, movie_id):
    Movie_detail = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(Movie_detail=Movie_detail.serialize)


@app.route('/genre/JSON')
def genresJSON():
    genres = session.query(Genre).all()
    return jsonify(genres=[r.serialize for r in genres])


# Show all genres
@app.route('/')
@app.route('/genre/')
def showGenres():
    genres = session.query(Genre).order_by(asc(Genre.name))
    if 'username' not in login_session:   # local permission
        return render_template('publicgenre.html', genres=genres)
    else:
        return render_template('genre.html', genres=genres)


# Create a new genre
@app.route('/genre/new/', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:  # local permission
        return redirect('/login')

    if request.method == 'POST':
        newGenre = Genre(
            name=request.form['name'],
            user_id=login_session['user_id']
        )
        session.add(newGenre)
        flash('New Genre %s Successfully Created' % newGenre.name)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')


# Edit a genre
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
    editedGenre = session.query(Genre).filter_by(id=genre_id).one()
    if 'username' not in login_session:
        return redicrect('/login')

    if editedGenre.user_id != login_session['user_id']:
        return """
            <script>function myFunction() {alert('You are not authorized to
            edit this genre. PLease create your own genre in order to edit.');}
            </script><body onload ='myFunction()''>
        """

    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            flash('Genre Successfully Edited %s' % editedGenre.name)
            return redirect(url_for('showGenres'))
    else:
        return render_template('editGenre.html', genre=editedGenre)


# Delete a genre
@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    genreToDelete = session.query(Genre).filter_by(id=genre_id).one()
    if genreToDelete.user_id != login_session['user_id']:
        return """
            <script>function myFunction() {alert('You are not authorized
            to delete this genre. PLease create your own genre in order
            to delete.');}</script><body onload ='myFunction()''>
        """

    if request.method == 'POST':
        session.delete(genreToDelete)
        flash('%s Successfully Deleted' % genreToDelete.name)
        session.commit()
        return redirect(url_for('showGenres', genre_id=genre_id))
    else:
        return render_template('deleteGenre.html', genre=genreToDelete)


# Show movies in a genre
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/movie/')
def showMovie(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    movies = session.query(Movie).filter_by(genre_id=genre_id).all()
    creator = getUserInfo(genre.user_id)

    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template(
            'publicmovie.html',
            movies=movies,
            genre=genre,
            creator=creator
        )
    else:
        return render_template(
            'movie.html',
            movies=movies,
            genre=genre,
            creator=creator
        )


# Create a new movie
@app.route('/genre/<int:genre_id>/movie/new/', methods=['GET', 'POST'])
def newMovie(genre_id):
    if 'username' not in login_session:
        return redicrect('/login')

    genre = session.query(Genre).filter_by(id=genre_id).one()

    if login_session['user_id'] != genre.user_id:
        return """
        <script>function myFunction() {alert('You are not authorized to
        add movies to this genre. PLease create your own genre in order
        to add movies.');}</script><body onload ='myFunction()''>
        """

    if request.method == 'POST':
        if request.form['name']:
            newMovie = Movie(
                name=request.form['name'],
                description=request.form['description'],
                director=request.form['director'],
                starring=request.form['starring'],
                genre_id=genre_id
            )
            session.add(newMovie)
            flash('New Movie %s Successfully Created' % (newMovie.name))
            session.commit()
        return redirect(url_for('showMovie', genre_id=genre_id))
    else:
        return render_template('newmovie.html', genre_id=genre_id)


# Edit a movie
@app.route(
    '/genre/<int:genre_id>/movie/<int:movie_id>/edit',
    methods=['GET', 'POST']
)
def editMovie(genre_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedMovie = session.query(Movie).filter_by(id=movie_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()
    if login_session['user_id'] != genre.user_id:
        return """
        <script>function myFunction() {alert('You are not authorized
        to edit movies to this genre. Please create your own genre in
        order to edit movies.');}</script><body onload='myFunction()''>
        """

    if request.method == 'POST':
        if request.form['name']:
            editedMovie.name = request.form['name']
        if request.form['description']:
            editedMovie.description = request.form['description']
        if request.form['director']:
            editedMovie.director = request.form['director']
        if request.form['starring']:
            editedMovie.starring = request.form['starring']
            session.add(editedMovie)
            session.commit()
            flash('Movie Successfully Edited')
        return redirect(url_for('showMovie', genre_id=genre_id))
    else:
        return render_template(
            'editmovie.html',
            genre_id=genre_id,
            movie_id=movie_id,
            movie=editedMovie
        )


# Delete a movie
@app.route(
    '/genre/<int:genre_id>/movie/<int:movie_id>/delete',
    methods=['GET', 'POST']
)
def deleteMovie(genre_id, movie_id):
    if 'username' not in login_session:
        return redirect('/login')
    movieToDelete = session.query(Movie).filter_by(id=movie_id).one()
    genre = session.query(Genre).filter_by(id=genre_id).one()

    if login_session['user_id'] != genre.user_id:
        return """<script>function myFunction() {alert('You are not authorized
        to delete movies to this genre. Please create your own genre in order
        to delete movies.');}</script><body onload='myFunction()''>
        """

    if request.method == 'POST':
        session.delete(movieToDelete)
        session.commit()
        flash('Movie Successfully Deleted')
        return redirect(url_for('showMovie', genre_id=genre_id))
    else:
        return render_template(
            'deleteMovie.html',
            genre_id=genre_id,
            movie_id=movie_id,
            movie=movieToDelete
        )


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False, ssl_context='adhoc')
