from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators, PasswordField, BooleanField, SelectField, \
    DateField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    dcpt = TextAreaField('Description')
    submit = SubmitField('Create New Artist')


class NewEventForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    startTime = DateField('time', format='%Y-%m-%d')
    venue = SelectField('venue',coerce=int, validators=[DataRequired()])
    artists = SelectMultipleField('Artists', coerce=int, choices=[], validators=[DataRequired()], render_kw={"multiple": "true"})
    submit = SubmitField('Create New Event')


class NewVenueForm(FlaskForm):
    venueName = StringField('Venue Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()] )
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

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')