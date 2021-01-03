from constants import Genres


def prepare_venues_data(venues, places):
    locales = []
    for place in places:
        locales.append(
            {
            'city': place.city,
            'state': place.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
            }
            for venue in venues if
                venue.city == place.city and venue.state == place.state]
            })
    
    return locales


def prepare_single_venue_data(venue_info, past_shows, upcoming_shows):

    return {
        "id": venue_info.id,
        "name": venue_info.name,
        "genres": [Genres[genre] for genre in venue_info.genres],
        "address": venue_info.address,
        "city": venue_info.city,
        "state": venue_info.state,
        "phone": venue_info.phone,
        "website": venue_info.website,
        "facebook_link": venue_info.facebook_link,
        "seeking_talent": venue_info.seeking_talent,
        "seeking_description": venue_info.seeking_description,
        "image_link": venue_info.image_link,
        "upcoming_shows": [
            {
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } 
            for artist, show in upcoming_shows
        ],
        "past_shows": [
            {
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } 
            for artist, show in past_shows
        ],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

def prepare_single_artist_data(artist_info, past_shows, upcoming_shows):

    return {
        "id": artist_info.id,
        "name": artist_info.name,
        "genres": [Genres[genre] for genre in artist_info.genres],
        "city": artist_info.city,
        "state": artist_info.state,
        "phone": artist_info.phone,
        "website": artist_info.website,
        "facebook_link": artist_info.facebook_link,
        "seeking_venue": artist_info.seeking_venue,
        "seeking_description": artist_info.seeking_description,
        "image_link": artist_info.image_link,
        "upcoming_shows": [
            {
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } 
            for venue, show in upcoming_shows
        ],
        "past_shows": [
            {
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            } 
            for venue, show in past_shows
        ],
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
