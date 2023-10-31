from urllib import request

from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import NewArtistForm, LoginForm, RegistrationForm
from app.models import User


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
        render_template('new_artist.html', title="New Artist", form=new_form)

    return render_template('new_artist.html', title="New Artist", form=form)


@app.route('/desc')
def desc():
    return render_template('desc.html', title='Gunna Description')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
