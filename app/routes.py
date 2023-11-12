import datetime
from datetime import datetime
from datetime import date
from urllib import request

from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import NewArtistForm, LoginForm, RegistrationForm, NewEventForm, NewVenueForm, EmptyForm
from app.models import User, Artist, Event, Venue
from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/artist_list')
def artistList():
    artist_list = Artist.query.all()
    event_list = Event.query.all()
    venue_list = Venue.query.all()
    return render_template('artist_list.html', artist_list=artist_list, event_list=event_list, venue_list=venue_list)


@app.route('/new_artist', methods=['GET', 'POST'])
def new_artists():
    form = NewArtistForm()
    results = {}
    if form.validate_on_submit():
        results = {
            "Name": request.form.get("name"),
            "Hometown": request.form.get("hometown"),
            "Description": request.form.get("dcpt")
        }
        new_artist = Artist(name=results['name'], hometown=results['hometown'], dcpt=results['dcpt'])
        db.session.add(new_artist)
        db.session.commit()
        return redirect('/')
    return render_template('new_artist.html', form=form)


@app.route('/new_event', methods=['GET', 'POST'])
def new_event():
    form = NewEventForm()
    form.artists.choices = [(a.id, a.name) for a in Artist.query.all()]
    form.venue.choices = [(v.id, v.name) for v in Venue.query.all()]
    if form.validate_on_submit():
        event_date = form.time.data
        new_event = Event(eventName=form.name.data, startTime=event_date, venue_id=form.venue.data)

        artist_ids = form.artists.data

        if not isinstance(artist_ids, (list, tuple)):
            artist_ids = [artist_ids]
        all_artists = Artist.query.all()
        for artist in all_artists:
            for id in artist_ids:
                if id == artist.id:
                    new_event.artists.append(artist)

        db.session.add(new_event)
        db.session.commit()
        return redirect('/')
    return render_template('new_event.html', form=form)


@app.route('/new_venue', methods=['GET', 'POST'])
def new_venue():
    form = NewVenueForm()
    results = {}
    if form.validate_on_submit():
        results = {
            "venueName": request.form.get("venueName"),
            "Address": request.form.get("address"),
            "Capacity": request.form.get("capacity")
        }
        new_venue = Venue(venueName=results['venueName'], address=results['address'], capacity=results['capacity'])
        db.session.add(new_venue)
        db.session.commit()
        return redirect('/')
    return render_template('new_artist.html', form=form)


@app.route('/artist/<name>', methods=['GET', 'POST'])
def artist(name):
    event_list = []
    get_artist = Artist.query.filter_by(artistName=name).first()

    if not get_artist:
        return "Artist not found", 404

    artist_info = {
        'id': get_artist.id,
        "name": get_artist.artistName,
        "hometown": get_artist.hometown,
        "description": get_artist.dcpt
    }

    for event in get_artist.events:
        event_list.append(event.name)

    return render_template('artist.html', title='Artist', artist_info=artist_info, event_list=event_list)


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


def dummy_database():
    fake = Faker()

    art1 = Artist(name=fake.name(), hometown=fake.city(), bio=fake.text())
    art2 = Artist(name=fake.name(), hometown=fake.city(), bio=fake.text())
    art3 = Artist(name=fake.name(), hometown=fake.city(), bio=fake.text())
    art4 = Artist(name=fake.name(), hometown=fake.city(), bio=fake.text())
    art5 = Artist(name=fake.name(), hometown=fake.city(), bio=fake.text())

    db.session.add_all([art1, art2, art3, art4, art5])
    db.session.commit()

    ven1 = Venue(venueName='The 307 Lounge', address=fake.address(), capacity=2000)
    ven2 = Venue(venueName='The 40Dub', address=fake.address(), capacity=8000)
    ven3 = Venue(venueName='Neon Lights', address=fake.address(), capacity=3000)
    ven4 = Venue(venueName='Vice City', address=fake.address(), capacity=950)
    ven5 = Venue(venueName='Weltons Club', address=fake.address(), capacity=2200)

    db.session.add_all([ven1, ven2, ven3, ven4, ven5])
    db.session.commit()

    event1 = Event(eventName="Lets Get Lit", startTime=date(2023, 5, 11), venue_id=ven2.id, artists=[art1, art2, art3])
    event2 = Event(eventName="The 24/7 Concert", startTime=date(2024, 7, 22), venue_id=ven3.id,
                   artists=[art1, art2, art3, art4, art5])
    event3 = Event(eventName="FameLab Concert", startTime=date(2024, 5, 30), venue_id=ven3.id, artists=[art3, art5])
    event4 = Event(eventName="333 Forever", startTime=date(2024, 6, 4), venue_id=ven1.id, artists=[art2, art4, art5])
    event5 = Event(eventName="Classy&Fancy", startTime=date(2024, 1, 5), venue_id=ven4.id, artists=[art2, art5])
    event6 = Event(eventName="Jeff's Night", startTime=date(2023, 12, 16), venue_id=ven5.id, artists=[art3, art4])
    event7 = Event(eventName="WokeUpAHourAgo", startTime=date(2023, 11, 7), venue_id=ven5.id, artists=[art2, art4, art5])

    db.session.add_all([event1, event2, event3, event4, event5, event6, event7])
    db.session.commit()
    return render_template('index.html')


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user.html', user=user, form=form)