from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Dre'}
    return render_template('index.html', title='Home', user=user)


@app.route('/artists')
def artists():
    return render_template('artists.html', title='Artists')


@app.route('/new_artists')
def new_artists():
    return "Under Construction. Coming Soon..."


@app.route('/desc')
def desc():
    return render_template('desc.html', title='Gunna Description')
