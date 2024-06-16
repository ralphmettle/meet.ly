from app import create_app, db
from models import User
from flask_bcrypt import Bcrypt
from uuid import uuid4

def add_test_user():
    app = create_app()
    bcrypt = Bcrypt(app)
    
    with app.app_context():        
        # Check if the user already exists
        user = User.query.filter_by(username='test').first()
        if not user:
            # Create the test user
            test_user = User(
                id=str(uuid4()),  # Generate a new UUID for the user ID
                username='test',
                email='test@test.com',
                password=bcrypt.generate_password_hash('test').decode('utf-8')
            )
            db.session.add(test_user)
            db.session.commit()
            print(f'Test user created: {test_user}')
        else:
            print('Test user already exists.')

def delete_test_user():
    app = create_app()
    
    with app.app_context():
        # Check if the user already exists
        user = User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print('Test user deleted.')
        else:
            print('Test user does not exist.')


if __name__ == '__main__':
    add_test_user()

