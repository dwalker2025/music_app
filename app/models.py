from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

db = SQLAlchemy()
from wtforms import ValidationError

import music_app
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_username(self, username):
        if not username.data.isalnum():
            raise ValidationError('Must use characters and digits only.')

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password is too short.')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artistName = db.Column(db.String(100), nullable=False)
    hometown = db.Column(db.String(300), nullable=False)
    bio = db.Column(db.String(1000), nullable=False)
    events = db.relationship('Event', secondary='artist_event_association', back_populates='artists')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venueName = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    events = db.relationship('Event', back_populates='venue')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    venue = db.relationship('Venue', back_populates='events')
    artists = db.relationship('Artist', secondary='artist_event_association', back_populates='events')

    def __repr__(self):
        return '<User {}>'.format(self.username)

artist_event_association = db.Table(
    'artist_event',
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)