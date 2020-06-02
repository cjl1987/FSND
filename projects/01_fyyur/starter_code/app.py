#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from datetime import date


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):              
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)   
    seeking_description = db.Column(db.String())    
    genres = db.Column(db.ARRAY(db.String), nullable=False)

    artists = db.relationship('Artist', secondary='show')
    shows = db.relationship('Show', cascade='all,delete-orphan', backref=db.backref('venues', single_parent=True, cascade='all,delete-orphan'), lazy=True)

# Link for PSQL INSERT:  
# INSERT INTO venue (id, name, city, state, address, phone, image_link, facebook_link, website, seeking_talent, seeking_description, genres) VALUES (1, 'The Musical Hop','San Francisco', 'CA','1015 Folsom Street','123-123-1234','https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60','https://www.facebook.com/TheMusicalHop','https://www.themusicalhop.com',True, 'We are on the lookout for a local artist to play every two weeks. Please call us.','{"Jazz", "Reggae", "Swing", "Classical", "Folk"}');
# INSERT INTO venue (id, name, city, state, address, phone, image_link, facebook_link, website, seeking_talent, seeking_description, genres) VALUES (2, 'The Dueling Pianos Bar','New York', 'NY','335 Delancey Street','914-003-1132','https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80','https://www.facebook.com/theduelingpianos','https://www.theduelingpianos.com', False, False,'{"Classical", "R&B", "Hip-Hop"}');
# INSERT INTO venue (id, name, city, state, address, phone, image_link, facebook_link, website, seeking_talent, seeking_description, genres) VALUES (3, 'Park Square Live Music & Coffee','San Francisco', 'CA','34 Whiskey Moore Ave','415-000-1234','https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80','https://www.facebook.com/ParkSquareLiveMusicAndCoffee','https://www.parksquarelivemusicandcoffee.com', False, False,'{"Rock n Roll", "Jazz", "Classical", "Folk"}');


class Artist(db.Model):                             
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))      
    website=db.Column(db.String(120))
    seeking_venue =db.Column(db.Boolean, default=False)
    seeking_description=db.Column(db.String())

    venues = db.relationship('Venue', secondary='show')
    shows = db.relationship('Show', backref='artists') 

# Link for PSQL INSERT:  
# INSERT INTO artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (4, 'Guns N Petals', 'San Francisco', 'CA', '326-123-5000', '{"Rock n Roll"}','https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80', 'https://www.facebook.com/GunsNPetals', 'https://www.gunsnpetalsband.com', True,'Looking for shows to perform at in the San Francisco Bay Area!' );
# INSERT INTO artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (5, 'Matt Quevedo', 'New York', 'NY', '300-400-5000', '{"Jazz"}','https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', 'https://www.facebook.com/mattquevedo923251523',NULL, False, NULL);
# INSERT INTO artist (id, name, city, state, phone, genres, image_link, facebook_link, website, seeking_venue, seeking_description) VALUES (6, 'The Wild Sax Band', 'San Francisco', 'CA', '432-325-5432', '{"Jazz","Classical"}', 'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',NULL,NULL, False, NULL);    


class Show(db.Model):
  __tablename__ = 'show'
  
  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable= False)

  venue = db.relationship('Venue')
  artist = db.relationship('Artist')


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

  data=[]
  venues_temp=[]
  temp=[]
  
  state = None
  city = None 

  venues = Venue.query.order_by('state','city').all()


  for venue in venues:
    venue_temp={
      'id':venue.id, 
      'name':venue.name,
      'num_upcoming_shows': Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>=datetime.now()).count(), 
    }
        
    if state==venue.state and city==venue.city:
          venues_temp.append(venue_temp)

    else:
      if state is not None:
        data=data+temp
      
      venues_temp=[venue_temp]
      temp = [{
      "city":venue.city, 
      "state":venue.state,
      "venues":venues_temp,
      }]
      

    state=venue.state
    city=venue.city

  data=data+temp
    
  return render_template('pages/venues.html', areas=data)

 

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_str = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.ilike('%'+search_str+'%')).all()

  data=[]
  
  for venue in venues: 
    tmp={}
    tmp['id']=venue.id
    tmp['name']=venue.name
    tmp['num_upcoming_shows']= Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).count() 
        
    data.append(tmp)
    
  response={
    "count": len(venues),
    "data": data,        
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  #get basic venue data
  venue=Venue.query.get(venue_id)

  past_shows = []
  upcoming_shows = []    

  up_shows_tmp = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>=datetime.now()).all()
  past_shows_tmp = Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time<datetime.now()).all() 


  for show in past_shows_tmp:
    tmp = {}
    tmp['artist_id'] = show.artist_id      
    tmp['artist_name'] = Artist.query.get(show.artist_id).name
    tmp['artist_image_link']=Artist.query.get(show.artist_id).image_link
    tmp['start_time']=str(show.start_time)
    past_shows.append(tmp)


  for show in up_shows_tmp:
    tmp = {}
    tmp['artist_id'] = show.artist_id      
    tmp['artist_name'] = Artist.query.get(show.artist_id).name
    tmp['artist_image_link']=Artist.query.get(show.artist_id).image_link
    tmp['start_time']=str(show.start_time)
    upcoming_shows.append(tmp)


  data={
    "id": venue.id, 
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count':len(upcoming_shows),
  }

  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error = False

  try: 
    venue = Venue()
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.image_link = request.form.get('image_link')
    venue.facebook_link = request.form.get('facebook_link')
    venue.website = request.form.get('website')                        
    seeking_talent_tmp = request.form.get('seeking_talent')   
    if seeking_talent_tmp == 'y':
      venue.seeking_talent = True
    if seeking_talent_tmp == 'n':
      venue.seeking_talent = False
    venue.seeking_description = request.form.get('seeking_description')   
    form = VenueForm(request.form)
    venue.genres = form.genres.data
    db.session.add(venue)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if not error: 
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else: 
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

  
  return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete', methods=['get'])
def delete_venue(venue_id):

  error = False
  print("---------Reched Venue Delete PATH-----------")
  try:
    venue=Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash('The venue was deleted!')
  
  except:
    error = True
    db.session.rollback()
    flash('Deleting the venue did not work!')
    print("Exception caught")

  finally: 
    db.session.close()

  return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data=Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_str = request.form.get('search_term')
  artists = Artist.query.filter(Artist.name.ilike('%'+search_str+'%')).all()
  

  data=[]
  
  for artist in artists: 
    tmp={}
    tmp['id']=artist.id
    tmp['name']=artist.name
    tmp['num_upcoming_shows']= Show.query.filter(Show.artist_id==artist.id).filter(Show.start_time>datetime.now()).count() 
    #tmp['num_upcoming_shows']=db.session.query(Venue).join(Show, Show.venue_id==venue.id).filter(Show.start_time>now).all()
    #tmp['num_upcoming_shows']=Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now().all()     
    #len(db.session.query(Show).filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all())   # Das hier funktioniert. 
    #len(Show.query.filter(Show.venue_id==venue.id).filter(Show.start_time>datetime.now()).all())
        
    data.append(tmp)
    

  response={
    "count": len(artists),
    "data": data,  
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
 
  #get basic artist data 
  artist=Artist.query.get(artist_id)

  past_shows = []
  upcoming_shows = []    

  up_shows_tmp = Show.query.filter(Show.artist_id==artist.id).filter(Show.start_time>=datetime.now()).all()
  past_shows_tmp = Show.query.filter(Show.artist_id==artist.id).filter(Show.start_time<datetime.now()).all() 


  for show in past_shows_tmp:
    tmp = {}
    tmp['venue_id'] = show.venue_id      
    tmp['venue_name'] = Venue.query.get(show.venue_id).name
    tmp['venue_image_link']=Venue.query.get(show.venue_id).image_link
    tmp['start_time']=str(show.start_time)
    past_shows.append(tmp)

  for show in up_shows_tmp:
    tmp = {}
    tmp['venue_id'] = show.venue_id      
    tmp['venue_name'] = Venue.query.get(show.venue_id).name
    tmp['venue_image_link']=Venue.query.get(show.venue_id).image_link
    tmp['start_time']=str(show.start_time)
    upcoming_shows.append(tmp)

  data={
    "id": artist.id, 
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count':len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=data)



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  error = False
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.image_link = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')
    artist.website = request.form.get('website')                              
    seeking_venue_tmp = request.form.get('seeking_venue')   
    if seeking_venue_tmp == 'y':
      artist.seeking_venue = True
    if seeking_venue_tmp == 'n':
      artist.seeking_venue = False
    artist.seeking_description = request.form.get('seeking_description')      
    form = ArtistForm(request.form)
    artist.genres = form.genres.data
    db.session.add(artist)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      return render_template('errors/500.html')
    else:
       return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:   
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form.get('address')
    venue.phone = request.form['phone']
    venue.image_link = request.form.get('image_link')
    venue.facebook_link = request.form.get('facebook_link')
    venue.website = request.form.get('website')                              
    seeking_talent_tmp = request.form.get('seeking_talent')   
    if seeking_talent_tmp == 'y':
      venue.seeking_talent = True
    if seeking_talent_tmp == 'n':
      venue.seeking_talent = False  
    venue.seeking_description = request.form.get('seeking_description')      
    form = VenueForm(request.form)
    venue.genres = form.genres.data
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      return render_template('errors/500.html')
    else:
      return redirect(url_for('show_venue', venue_id=venue_id))



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  error = False

  try: 
    artist = Artist()
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.image_link = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')
    artist.website = request.form.get('website')                              
    seeking_venue_tmp = request.form.get('seeking_venue')   
    if seeking_venue_tmp == 'y':
      artist.seeking_venue = True
    if seeking_venue_tmp == 'n':
      artist.seeking_venue = False
    artist.seeking_description = request.form.get('seeking_description')      
    form = ArtistForm(request.form)
    artist.genres = form.genres.data
    db.session.add(artist)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if not error: 
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else: 
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  
  shows = Show.query.all()

  data=[]

  for show in shows: 
    show_tmp = {}
    show_tmp['venue_id']=show.venue_id
    show_tmp['venue_name']=Venue.query.get(show.venue_id).name
    show_tmp['artist_id']= show.artist_id
    show_tmp['artist_name']=Artist.query.get(show.artist_id).name
    show_tmp['artist_image_link']=Artist.query.get(show.artist_id).image_link
    show_tmp['start_time']=show.start_time.isoformat()  
    data.append(show_tmp)
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  error = False

  try: 
    show = Show()
    show.artist_id = request.form.get('artist_id')
    show.venue_id = request.form.get('venue_id')
    show.start_time = request.form.get('start_time')

    db.session.add(show)
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  
  finally:
    db.session.close()
    if not error: 
      flash('Show was successfully listed!')
    else: 
      flash('An error occurred. Show could not be listed.')

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
