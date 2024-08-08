import googlemaps
import hashlib
import json
import os

from flask import flash, jsonify, render_template, request, redirect, url_for 
from flask_login import login_user, logout_user, current_user, login_required
from location_clustering import coordinate_builder, location_clustering
from gpt_api import client, MODEL
from models import User, UserLocation, Friendship
from sqlalchemy import or_

places_api_key = "AIzaSyDsqXAw5paGfj1xv-SvrJgOcaowqEo9W6Y"
gmaps = googlemaps.Client(key=places_api_key)

def config_views(app, db, bcrypt):

    @app.before_request
    def verification():
        if current_user.is_authenticated:
            if not current_user.welcomed and \
            request.endpoint not in ['welcome', 'logout', 'static', 'index']:
                return redirect(url_for('welcome'))
                   
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            user_location = UserLocation.query.filter_by(user_id=current_user.id).all()
        else:
            user_location = []
        return render_template('index.html', user_location=user_location)
    
    @app.route('/home')
    @login_required
    def home():
        if current_user.is_authenticated:
            return render_template('home.html', username=current_user.username)
        else:
            return render_template('home.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('home'))
            else:
                return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Check the database for the user with the given username if provided, otherwise check by email
            def find_db_user(username, email):
                if username is not None:
                    return User.query.filter_by(username=username).first()
                else: 
                    return User.query.filter_by(email=email).first()
            
            user = find_db_user(username, email)
            
            # Check if the user exists in the database and the password is correct
            if user is not None:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('home'))
            else:
                return f"Incorrect username or password.\nCredentials: {username}, {email}, {password}"
            
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            if current_user.is_authenticated:
                return redirect(url_for('index'))
            else:
                return render_template('register.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            def create_user_in_db(username, email, password):
                new_user = User(
                    username=username, 
                    email=email, 
                    password=bcrypt.generate_password_hash(password).decode('utf-8')
                    )
                db.session.add(new_user)
                db.session.commit()

            create_user_in_db(username, email, password)

        return redirect(url_for('login'))
    
    @app.route('/welcome', methods=['GET', 'POST'])
    @login_required
    def welcome():
        if request.method == 'GET':
            if current_user.welcomed:
                return redirect(url_for('home'))
            else:
                return render_template('welcome.html')
            
            # Get the profile picture and location of user
            # Possibly implement logic to select preferred vibes
        elif request.method == 'POST':
            # Get user profile picture if submitted
            # Name the file user.ID_profilepicture for storage in the database
            profile_picture = request.files.get('profile_picture')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            user = current_user

            process_profile_picture(profile_picture, user)

            if latitude and longitude:
                user_location = UserLocation(user_id=user.id, latitude=latitude, longitude=longitude)

                db.session.add(user_location)
            
            user.welcomed = True
            db.session.commit()
            return redirect(url_for('home'))

    @app.route('/forgot-password')
    def forgot_password():
        return f'The forgot password page is not yet implemented.'
        
    @app.route('/<username>')
    def user(username):
        user = User.query.filter_by(username=username).first()

        if user is None:
            return '404 Not Found', 404
        
        if current_user.is_authenticated and current_user.username == username:
            return render_template('profile.html', user=user, user_profile = True)
        else:
            return render_template('profile.html', user=user, user_profile = False)
    
    @app.route('/friends')
    @login_required
    def friends():
        return render_template('friends.html')
    
    @app.route('/memories')
    @login_required
    def memories():
        return render_template('memories.html')
    
    @app.route('/hangouts')
    @login_required
    def hangouts():
        return render_template('hangouts.html')
    
    @app.route('/hangouts/new')
    @login_required
    def new_hangout():
        return render_template('new_hangout.html')
    

    # Routes and functions for processing data from the front-end
    
    def get_extension(filename):
        if '.' in filename:
            extension = filename.split('.', 1)[1].lower()
            return extension
        else:
            raise ValueError('No file extension found.')
    
    def hashed_string(string):
        hashed = hashlib.sha256(string.encode())
        return hashed.hexdigest()

    def create_filename(filename, extension):
        return f'{filename}.{extension}'

    def process_profile_picture(profile_picture, user):
        picture_folder = 'static\images\profile_pictures'
        extensions = {'jpg', 'jpeg', 'png'}

        if profile_picture and get_extension(profile_picture.filename) in extensions:
            filename = create_filename(hashed_string(user.id), get_extension(profile_picture.filename))
            file_path = os.path.join(picture_folder, filename)
            print(f"Saving file to: {file_path}")

            profile_picture.save(file_path)
            
            user.profile_picture = filename
        else:
            user.profile_picture = None
            flash('Invalid file type. Please upload a .jpg, .jpeg, or .png file.')
            pass
    
    @app.route('/process-search-user', methods=['POST'])
    @login_required
    def process_search_user():
        data = request.get_json()
        search = data.get('username')
        
        # Query the database for users with the search term in their username, first name, or last name, with partial matches allowed
        results = User.query.filter(
            or_(
                User.username.like(f'%{search}%'),
                User.firstname.like(f'%{search}%'),
                User.lastname.like(f'%{search}%')
            )
        ).all()
        
        print(results)
        
        # Return a list of dictionaries containing the username, first name, and last name of each user
        return_users = [
            {
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname
            }
            for user in results
        ]

        if return_users:
            return jsonify(return_users), 200
        else:
            return jsonify({'message': 'No user found.'}), 400
    
    @app.route('/process-add-friend', methods=['POST'])
    @login_required
    def process_add_friend():
        data = request.get_json()
        friend_username = data.get('username')
        
        user_id = current_user.id
        friend_id = User.query.filter_by(username=friend_username).first().id
        
        if friend_id:
            if friend_id == user_id:
                return jsonify({'message': 'You cannot add yourself as a friend.'}), 400
            else:
                new_friendship = Friendship(user_id=user_id, friend_id=friend_id)
                db.session.add(new_friendship)
                db.session.commit()

                return jsonify({'message': 'Friend request sent.'}), 200
        else:
            return jsonify({'message': 'No username provided.'}), 400

    @app.route('/process-user_id-search-coords', methods=['POST'])
    @login_required
    def process_user_id_search_coords():
        data = request.get_json()
        usernames = data.get('usernames')
        
        if usernames:
            # Query database to get user_id, latitude, and longitude for each username
            user_info = {
                username: [
                    user.id,
                    [
                        user.location.latitude,
                        user.location.longitude
                    ]
                ]
                for username in usernames
                for user in User.query.filter_by(username=username).all()
            }
            
            if user_info:
                return jsonify(user_info), 200
            else:
                return jsonify({'message': 'No user data found.'}), 400
        else:
            user_info = None
            return jsonify({'message': 'No usernames provided.'}), 400
        
    @app.route('/process-hangout-prompt', methods=['POST'])
    @login_required
    def process_hangout_prompt():
        # Get the response from the request JSON object and extract the prompt into 'search_query'

        data = request.get_json()
        search_query = data.get('prompt')

        response  = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": f"Extract keywords from this text to be used to search the Google Places API: '{search_query}'. Respond *only* with a JSON object containing the keywords, nothing else, no annotations."},
            ],
            temperature=0,
        )

        # Extract the response from the API
        prompt_response = response.choices[0].message.content

        # Remove the markdown from the response
        if prompt_response.startswith('```json'):
            prompt_response = prompt_response[7:].strip()
        if prompt_response.endswith('```'):
            prompt_response = prompt_response[:-3].strip()

        response_dict = json.loads(prompt_response)
        keywords = response_dict.get('keywords')
        
        return jsonify(keywords), 200

    @app.route('/process-hangout-search', methods=['POST'])
    @login_required
    def process_hangout_search():
        # Get the response from the request JSON object and extract the keywords
        # Use the extracted keywords to search the Google Places API
        # Return the Places search result to be displayed on the front-end

        data = request.get_json()
        keywords = data.get('keywords')
        location = [51.5074, -0.1278]   

        # Use the keywords to search the Google Places API
        search_query = '+'.join([keyword.replace(' ', '-') for keyword in keywords])
        
        response = gmaps.places_nearby(location=location, radius=4000, keyword=search_query)

        return jsonify(response), 200
    
    @app.route('/process-place-info', methods=['POST'])
    @login_required
    def process_place_info():
        data = request.get_json()
        
        if 'results' in data:
            places = data['results'].get('results')
            # Extract the place name, place ID, and location coordinates as a dictionary
            place_info = {
                place.get('name'): [
                    place.get('place_id'),
                      [
                          place.get('geometry').get('location').get('lat'),
                          place.get('geometry').get('location').get('lng')
                      ]
                ]
                for place in places}
        else:
            place_info = None

        if place_info is not None:
            return jsonify(place_info), 200
        else:
            return jsonify({'message': 'No place data.'}), 400
