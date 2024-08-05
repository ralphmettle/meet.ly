from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from models import User, UserLocation

def config_views(app, db, bcrypt):

    @app.before_request
    def check_welcomed_status():
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
                return redirect(url_for('index'))
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
                    return redirect(url_for('index'))
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

            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            user = current_user

            if latitude and longitude:
                user_location = UserLocation(user_id=user.id, latitude=latitude, longitude=longitude)
                current_user.welcomed = True

                db.session.add(user_location)
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

    # @app.before_request
    # def check_login_status():
    #     endpoints = [
    #         'login',
    #         'register',
    #         'forgot_password',
    #         'home',
    #         'index'
    #     ]
        
    #     if not current_user.is_authenticated and \
    #         request.endpoint not in endpoints and \
    #         not request.endpoint.startswith('static'): # CSS won't work without this
    #             return redirect(url_for('login'))
