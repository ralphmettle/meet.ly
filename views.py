from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from models import User

def config_views(app, db, bcrypt):

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/home')
    def home():
        if current_user.is_authenticated:
            return render_template('home.html', username=current_user.username)
        else:
            return render_template('home.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
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
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
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
    def friends():
        return render_template('friends.html')
    
    @app.route('/memories')
    def memories():
        return render_template('memories.html')
    
    @app.route('/hangouts')
    def hangouts():
        return render_template('hangouts.html')

