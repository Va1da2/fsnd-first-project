from constants import Genres


def prepare_venues_data(current_date, raw_venues):
    data = {}
    for venue in raw_venues:
        city, state = venue.city, venue.state
        key = f"{city}-{state}"
        _, upcomming = past_future_shows(current_date, venue.show)
        if key in data:
            data[key]["venues"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(upcomming),
            })
        else:
            data[key] = {
                "city": venue.city,
                "state": venue.state,
                "venues": [{
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len(upcomming),
                }]
            } 
    return [venue for venue in data.values()]


def prepare_single_venue_data(current_date, venue):
    past_shows, future_shows = past_future_shows(current_date, venue.show)

    return {
        "id": venue.id,
        "name": venue.name,
        "genres": [Genres[genre] for genre in venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": future_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(future_shows),
    }

def prepare_single_artist_data(current_date, artist):
    past_shows, future_shows = past_future_shows(current_date, artist.show)

    return {
        "id": artist.id,
        "name": artist.name,
        "genres": [Genres[genre] for genre in artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": future_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(future_shows),
    }

def prepare_search_results(current_date, found_items):
    response = {"count": len(found_items), "data": []}
    for item in found_items:
        past_shows, future_shows = past_future_shows(current_date, item.show)
        response["data"].append({
            "id": item.id,
            "name": item.name,
            "num_upcoming_shows": len(future_shows),
        })
    
    return response

def past_future_shows(current_date, shows):
    if not shows:
        shows = []
    past = []
    upcomming = []
    for show in shows:
        formatted_show = {
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": str(show.start_time),
        }
        if show.start_time > current_date:
            upcomming.append(formatted_show)
        else:
            past.append(formatted_show)
    
    return past, upcomming
