from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class NewArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    hometown = StringField('Hometown', validators=[DataRequired()])
    dcpt = TextAreaField('Description')
    submit = SubmitField('Create New Artist')