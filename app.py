#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import datetime
import logging
from logging import Formatter, FileHandler

import babel
from flask import ( 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for
)
from flask_moment import Moment
from flask_wtf import FlaskForm as Form

from forms import VenueForm, ArtistForm, ShowForm
from models import app, db, Venue, Artist, Show
from helpers import (
  prepare_venues_data,
  prepare_single_venue_data,
  prepare_single_artist_data
)
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
moment = Moment(app)
# TODO: connect to a local postgresql database
db.init_app(app)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  areas = prepare_venues_data(venues, places)
  
  return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  found_venues = Venue.query.filter(Venue.name.ilike(f"%{search_term.lower().strip()}%")).all()
  response = {
    "count": len(found_venues),
    "data": found_venues,
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  current_date = datetime.datetime.utcnow()
  venue_info = Venue.query.filter_by(id = venue_id).first_or_404()
  previous_shows = db.session.query(Artist, Show)\
    .join(Show)\
    .join(Venue)\
    .filter(
      Show.venue_id == venue_id,
      Show.artist_id == Artist.id,
      Show.start_time < current_date
    )\
    .all()
  upcomming_shows = db.session.query(Artist, Show)\
    .join(Show)\
    .join(Venue)\
    .filter(
      Show.venue_id == venue_id,
      Show.artist_id == Artist.id,
      Show.start_time >= current_date
    )\
    .all()
  venue = prepare_single_venue_data(venue_info, previous_shows, upcomming_shows)

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  try:
    form.validate()

    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + venue + ' was successfully listed!')
  except Exception as e:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except Exception as e:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  #current_date = datetime.datetime.utcnow()
  search_term = request.form.get('search_term', '')
  found_artists = Artist.query.filter(Artist.name.ilike(f"%{search_term.lower().strip()}%")).all()
  response = {
    "count": len(found_artists),
    "data": found_artists
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  current_date = datetime.datetime.utcnow()
  artist_info = Artist.query.filter_by(id=artist_id).first_or_404()
  previous_shows = db.session.query(Venue, Show)\
    .join(Show)\
    .join(Artist)\
    .filter(
      Show.artist_id == artist_id,
      Show.venue_id == Venue.id,
      Show.start_time < current_date
    )\
    .all()
  upcomming_shows = db.session.query(Venue, Show)\
    .join(Show)\
    .join(Artist)\
    .filter(
      Show.artist_id == artist_id,
      Show.venue_id == Venue.id,
      Show.start_time >= current_date
    )\
    .all()
  artist = prepare_single_artist_data(artist_info, previous_shows, upcomming_shows)

  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.filter(Artist.id == artist_id).first()

  form.name.default = artist.name
  form.city.default = artist.city
  form.state.default = artist.state
  form.genres.default = artist.genres
  form.phone.default = artist.phone
  form.image_link.default = artist.image_link
  form.facebook_link.default = artist.facebook_link
  form.website.default = artist.website
  form.seeking_venue.default = artist.seeking_venue
  form.seeking_description.default = artist.seeking_description

  form.process()

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  try:
    form.validate()

    artist = Artist.query.filter(Artist.id == artist_id).first()
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = form.state.data.name
    artist.phone = form.phone.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.genres = [genre.name for genre in form.genres.data]
    artist.website = form.website.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
    
    db.session.commit()

  except Exception as e:
    print(e)
    db.session.rollback()
  
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.filter(Venue.id == venue_id).first()
  form.name.default = venue.name
  form.city.default = venue.city
  form.state.default = venue.state
  form.address.default = venue.address
  form.genres.default = venue.genres
  form.phone.default = venue.phone
  form.image_link.default = venue.image_link
  form.facebook_link.default = venue.facebook_link
  form.website.default = venue.website
  form.seeking_talent.default = venue.seeking_talent
  form.seeking_description.default = venue.seeking_description

  form.process()

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  try:
    form.validate()

    venue = Venue.query.filter(Venue.id == venue_id).first()
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = form.state.data.name
    venue.address = form.address.data
    venue.genres = [genre.name for genre in form.genres.data]
    venue.phone = form.phone.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()

  except Exception as e:
    print(e)

    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  try:
    form.validate()

    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data.name,
      phone=form.phone.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      genres=[genre.name for genre in form.genres.data],
      website=form.website.data,
      seeking_venue=form.seeking_venue.data,
      seeking_description=form.seeking_description.data,
    )
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  except Exception as e:
    print(e)
    db.session.rollback()
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  formatted_shows = []
  for show in shows:
    formatted_shows.append(
      {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
      }
    )

  return render_template('pages/shows.html', shows=formatted_shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  try:
    form.validate()

    show = Show(
      start_time=form.start_time.data,
      venue_id=form.venue_id.data,
      artist_id=form.artist_id.data,
    )

    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception as e:
    print(e)
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
