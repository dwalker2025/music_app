from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, PasswordField, BooleanField, SelectField, \
    DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    dcpt = TextAreaField('Description')
    submit = SubmitField('Create New Artist')


class NewEventForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    startTime = DateField('Start Time', validators=[DataRequired()])
    venues = ['25/8', "Ben's NightClub", 'LIveLife', 'FortyForty',
              "Dawns", "the Spotlight", "the Spot19", "Venice Lights", "Jake&Allies", "Bensons"]
    select_field = SelectField('Select a venue:', choices=venues)
    submit = SubmitField('Create New Event')


class NewVenueForm(FlaskForm):
    venueName = StringField('Event Name', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
    city = StringField('city', validators=[DataRequired()])
    capacity = IntegerField('capacity', validators=[DataRequired()] )
    select_field = SelectField('Select a state:', choices=states)
    submit = SubmitField('Create New Venue')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
