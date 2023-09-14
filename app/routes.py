from flask import render_template, flash
from app import app
from app.forms import NewArtistForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Dre'}
    return render_template('index.html', title='Home', user=user)


@app.route('/artists')
def artists():
    artists = ['Gunna', "Lil Baby", "Travis Scott", "SSGKOBE", "Future", "Kodak Black"]
    return render_template('artists.html', title='Artists', artists=artists)


@app.route('/new_artists', methods=['GET', 'POST'])
def new_artists():
    form = NewArtistForm()
    if form.validate_on_submit():
        flash("New Artist {} Created!".format(form.name.data))
        new_form = NewArtistForm()
        render_template('new_artists.html', title="New Artist", form=new_form)

    return render_template('new_artists.html', title="New Artist", form=form)


@app.route('/desc')
def desc():
    return render_template('desc.html', title='Gunna Description')
