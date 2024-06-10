from flask import Flask, render_template, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from models import User

def debug_config():
    return True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        
        def user_by_username(username):
            return User.query.filter_by(username=username).first()
        
        user = user_by_username(username)
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return 'Logged in successfully.'
        else:
            return 'Incorrect username or password.'

@app.route('/register')
def register():
    return 'The register page is not yet implemented.'

@app.route('/forgot-password')
def forgot_password():
    return 'The forgot password page is not yet implemented.'

@app.route('/user/<username>')
def user_page(username):
    '''
    Return the user page for the current logged-in user ONLY if the user
    is currently logged in and this is their session. Otherwise, return a
    403 error.
    '''

    '''
    if not current_user.is_authenticated:
        return '403 Forbidden', 403
    
    return render_template('user.html', username=username)
    '''
    return 'The user page is not yet implemented.'

@app.route('/user/profile/<username>')
def user_profile(username):
    '''
    # Return the public profile page for the given user
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)
    '''
    return 'The profile page is not yet implemented.'

if __name__ == '__main__':
    app.run(debug=debug_config())