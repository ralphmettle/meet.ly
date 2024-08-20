import googlemaps
import hashlib
import json
import os

from flask import flash, jsonify, render_template, request, redirect, url_for 
from flask_login import login_user, logout_user, current_user, login_required
from location_clustering import coordinate_builder, location_clustering
from gpt_api import client, MODEL
from models import User, UserLocation, Friendship, Hangout, HangoutAttendee
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

    def get_id_from_username(username):
        return User.query.filter_by(username=username).first().id

    def get_friends(user_id):
        user = db.session.get(User, user_id)

        if user:
            friends = user.friends + user.friend_of

            if not friends:
                return None
            else:
                return friends

    def get_friend_requests(user_id):
        user = db.session.get(User, user_id)

        if user:
            friend_requests = user.friend_requests

            if not friend_requests:
                return None
            else:
                return friend_requests

    def get_sent_requests(user_id):
        user = db.session.get(User, user_id)

        if user:
            sent_requests = user.sent_requests

            if not sent_requests:
                return None
            else:
                return sent_requests
    
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
        
        # Return a list of dictionaries containing the username, first name, and last name of each user
        return_users = [
            {
                'username': user.username,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'profile_picture': user.profile_picture
            }
            for user in results
        ]

        if return_users:
            return jsonify(return_users), 200
        else:
            return jsonify({'message': 'No user found.'}), 400
        
    @app.route('/process-get-friends', methods=['POST'])
    @login_required
    def process_get_friends():
        user_id = current_user.id
        friends = get_friends(user_id)
        
        friends_list = [
            {
                'username': friend.username,
                'firstname': friend.firstname,
                'lastname': friend.lastname,
                'profile_picture': friend.profile_picture
            }
            for friend in friends
        ]

        if friends_list:
            return jsonify(friends_list), 200
        else:
            return jsonify({'message': 'No friends added.'}), 400
        
    @app.route('/process-get-friend-requests', methods=['POST'])
    @login_required
    def process_get_friend_requests():
        user_id = current_user.id
        friend_requests = get_friend_requests(user_id)
        
        friend_requests_list = [
            {
                'username': friend.username,
                'firstname': friend.firstname,
                'lastname': friend.lastname,
                'profile_picture': friend.profile_picture
            }
            for friend in friend_requests
        ]

        if friend_requests_list:
            return jsonify(friend_requests_list), 200
        else:
            return jsonify({'message': 'No friend requests.'}), 400
        
    @app.route('/process-count-friend-requests', methods=['POST'])
    @login_required
    def process_count_friend_requests():
        user_id = current_user.id
        friend_requests = get_friend_requests(user_id)
        
        if friend_requests:
            return jsonify({'count': len(friend_requests)}), 200
        else:
            return jsonify({'count': 0}), 200
        
    @app.route('/process-get-sent-requests', methods=['POST'])
    @login_required
    def process_get_sent_requests():
        user_id = current_user.id
        sent_requests = get_sent_requests(user_id)
        
        sent_requests_list = [
            {
                'username': friend.username,
                'firstname': friend.firstname,
                'lastname': friend.lastname,
                'profile_picture': friend.profile_picture
            }
            for friend in sent_requests
        ]

        if sent_requests_list:
            return jsonify(sent_requests_list), 200
        else:
            return jsonify({'message': 'No sent requests.'}), 400
        
    @app.route('/process-send-friend-request', methods=['POST'])
    @login_required
    def process_send_friend_request():
        data = request.get_json()
        friend_username = data.get('username')
        
        user_id = current_user.id
        friend_id = User.query.filter_by(username=friend_username).first().id
        
        if \
        Friendship.query.filter_by(user_id=user_id, friend_id=friend_id).first() or \
        Friendship.query.filter_by(user_id=friend_id, friend_id=user_id).first():
            return jsonify({'message': 'Friend request already sent.'}), 400
                    
        elif user_id == friend_id:
            return jsonify({'message': 'Cannot send friend request to yourself.'}), 400
        
        else:
            new_friend_request = Friendship(user_id=user_id, friend_id=friend_id)
            db.session.add(new_friend_request)
            db.session.commit()
            return jsonify({'message': 'Friend request sent.'}), 200

    @app.route('/process-accept-friend-request', methods=['POST'])
    @login_required
    def process_accept_friend_request():
        data = request.get_json()
        friend_username = data.get('username')
        
        user_id = current_user.id
        friend_id = User.query.filter_by(username=friend_username).first().id
        
        friend_request = Friendship.query.filter_by(user_id=friend_id, friend_id=user_id).first()
        
        if friend_request:
            friend_request.accepted = True
            db.session.commit()
            return jsonify({'message': 'Friend request accepted.'}), 200
        else:
            return jsonify({'message': 'No friend request found.'}), 400
        
    @app.route('/process-decline-friend-request', methods=['POST'])
    @login_required
    def process_decline_friend_request():
        data = request.get_json()
        friend_username = data.get('username')
        
        user_id = current_user.id
        friend_id = User.query.filter_by(username=friend_username).first().id
        
        friend_request = Friendship.query.filter_by(user_id=friend_id, friend_id=user_id).first()
        
        if friend_request:
            db.session.delete(friend_request)
            db.session.commit()
            return jsonify({'message': 'Friend request declined.'}), 200
        else:
            return jsonify({'message': 'No friend request found.'}), 400

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

        # Extract the response from the OpenAI API
        prompt_response = response.choices[0].message.content

        # Remove the markdown from the response
        if prompt_response.startswith('```json'):
            prompt_response = prompt_response[7:].strip()
        if prompt_response.endswith('```'):
            prompt_response = prompt_response[:-3].strip()

        response_dict = json.loads(prompt_response)
        keywords = response_dict.get('keywords')
        
        return jsonify(keywords), 200
    
    @app.route('/process-review-summary', methods=['POST'])
    @login_required
    def process_review_summary():
        data = request.get_json()
        reviews = data.get('reviews')

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": f"I am going to pass a JSON object with some reviews of a place from Google Places. Generate a single summary made from the following reviews: {reviews} and return it as a JSON object *only*."},
            ],
            temperature=0,
        )

        prompt_response = response.choices[0].message.content

        if prompt_response.startswith('```json'):
            prompt_response = prompt_response[7:].strip()
        if prompt_response.endswith('```'):
            prompt_response = prompt_response[:-3].strip()
        
        return jsonify(prompt_response), 200

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
            # Extract the place name, place ID, location coordinates, and photo reference as a dictionary
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
        
    @app.route('/process-get-place-photo', methods=['POST'])
    @login_required
    def process_get_place_photo():
        data = request.get_json()
        place_info = data.get('place_info')

        if not place_info:
            return jsonify({"error": "No place information provided."}), 400

        photo_responses = {}

        for place_id, info in place_info.items():
            photo_reference = info[2]  # Assuming [2] is the photo_reference
            if photo_reference:
                try:
                    # Fetch the photo from Google Places API
                    response = gmaps.places_photo(photo_reference=photo_reference, max_width=400)
                    if response.status_code == 200:
                        photo_responses[place_id] = {
                            'photo_url': response.url,
                            'status': 'success'
                        }
                    else:
                        photo_responses[place_id] = {
                            'error': f"Failed to retrieve photo for place ID {place_id}",
                            'status': 'failed'
                        }
                except Exception as e:
                    photo_responses[place_id] = {
                        'error': str(e),
                        'status': 'failed'
                    }
            else:
                photo_responses[place_id] = {
                    'error': f"No photo reference provided for place ID {place_id}",
                    'status': 'failed'
                }

        return jsonify(photo_responses), 200  # Correctly return the 'photo_responses' dictionary
    
    @app.route('/process-add-hangout', methods=['POST'])
    @login_required
    def process_add_hangout():
        try:
            data = request.get_json()
            hangout_name = data.get('hangoutName')
            place_id = data.get('placeId')
            place_name = data.get('placeName')
            place_address = data.get('placeAddress')
            place_review_summary = data.get('placeReviewSummary')
            place_photo_url = data.get('placePhotoUrl')
            place_maps_link = data.get('placeMapsLink')

            user_id = current_user.id
            is_creator = True

            new_hangout = Hangout(
                user_id=user_id,
                is_creator=is_creator,
                name = hangout_name,
                place_name=place_name,
                place_address=place_address,
                place_review_summary=place_review_summary,
                place_id=place_id,
                place_photo_url=place_photo_url,
                place_maps_link=place_maps_link
            )

            db.session.add(new_hangout)
            db.session.flush()
            
            invitees = data.get('invitees')

            if invitees:
                invitee_ids = [get_id_from_username(username) for username in invitees]
                invitee_ids.append(user_id)
                
                for invitee_id in invitee_ids:
                    new_invitee = HangoutAttendee(hangout_id=new_hangout.id, user_id=invitee_id)
                    db.session.add(new_invitee)
                    
            db.session.commit()
            return jsonify({'message': 'Hangout created successfully.'}), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        
    @app.route('/process-search-friends', methods=['POST'])
    @login_required
    def process_search_friends():
        data = request.get_json()
        search = data.get('search')

        if not search:
            return jsonify({'message': 'No query provided.'}), 400
        
        friends = get_friends(current_user.id)

        if friends:
            friends_list = [
                {
                    'username': friend.username,
                    'firstname': friend.firstname,
                    'lastname': friend.lastname,
                    'profile_picture': friend.profile_picture
                }
                for friend in friends
                if search.lower() in friend.username.lower()
            ]
            return jsonify(friends_list), 200
        else:
            friends_list = None
            return jsonify({'message': 'No friends found.'}), 400

        
    @app.route('/process-get-hangouts', methods=['POST'])
    @login_required
    def process_get_hangouts():
        user_id = current_user.id
        hangouts = Hangout.query.filter_by(user_id=user_id).all()
        
        hangouts_list = [
            {
                'id': hangout.id,
                'name': hangout.name,
                'place_name': hangout.place_name,
                'place_address': hangout.place_address,
                'place_review_summary': hangout.place_review_summary,
                'place_photo_url': hangout.place_photo_url,
                'place_maps_link': hangout.place_maps_link
            }
            for hangout in hangouts
        ]

        if hangouts_list:
            return jsonify(hangouts_list), 200
        else:
            return jsonify({'message': 'No hangouts found.'}), 400
        
    #TESTING
    @app.route('/process-get-location_cluster', methods=['POST'])
    @login_required
    def process_get_location_cluster():
        data = request.get_json()
        invited_users = data.get('usernames')
        
        # Get the location of the current user from user_location table by user_id
        user_location = UserLocation.query.filter_by(user_id=current_user.id).first()
        user_coords = [user_location.latitude, user_location.longitude]

        # Get the location info of invited users
        if invited_users:
            invited_user_info = [
                [username, User.query.filter_by(username=username).first().id] 
                for username in invited_users
            ]

            invited_user_locations = {
                username: [
                    UserLocation.query.filter_by(user_id=user_id).first().latitude,
                    UserLocation.query.filter_by(user_id=user_id).first().longitude
                ]
                for username, user_id in invited_user_info
            }
            
            # Combine the user location with the invited user locations
            invited_user_locations[current_user.username] = user_coords

            coordinate_set = list(invited_user_locations.values())

            # Get central coordinates via location_clustering function
            central = location_clustering(coordinate_set)

            return jsonify(central), 200
        else:
            return jsonify({'message': 'No invited users.'}), 400

            

