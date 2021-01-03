from datetime import datetime

from flask_wtf import FlaskForm as Form
from markupsafe import escape
from wtforms import (
    StringField,
    SelectField,
    SelectMultipleField,
    DateTimeField,
    BooleanField,
    IntegerField
)
from wtforms.validators import DataRequired, InputRequired, AnyOf, URL, Regexp

from constants import Genres, States, coerce_for_enum
from form_validators import PhoneNumerValidator, RequiredPreviousField


class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id',  validators=[DataRequired()]
    )
    venue_id = IntegerField(
        'venue_id',  validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[InputRequired()],
        choices=[(state_opt.name, escape(state_opt)) for state_opt in States],
        coerce=coerce_for_enum(States)
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[(genre.name, escape(genre)) for genre in Genres],
        coerce=coerce_for_enum(Genres)
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_talent = BooleanField(
        'seeking_talent', default=False
    )
    seeking_description = StringField('seeking_description')


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[InputRequired()],
        choices=[(state_opt.name, escape(state_opt)) for state_opt in States],
        coerce=coerce_for_enum(States)
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone',
        validators=[Regexp(r'\d{3}-\d{3}-\d{4}'), PhoneNumerValidator()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[(genre.name, escape(genre)) for genre in Genres],
        coerce=coerce_for_enum(Genres)
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )
    seeking_venue = BooleanField(
        'seeking_venue', default=False
    )
    seeking_description = StringField(
        'seeking_description', validators=[RequiredPreviousField('seeking_venue')]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
