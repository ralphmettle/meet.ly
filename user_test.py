from app import create_app, db
from models import User
from flask_bcrypt import Bcrypt
from uuid import uuid4

def add_test_user():
    app = create_app()
    bcrypt = Bcrypt(app)
    
    with app.app_context():        
        # Check if the user already exists
        test = User.query.filter_by(username='dev_test').first()
        if not test:
            # Create the test user
            test_user = User(
                id=str(uuid4()),  # Generate a new UUID for the user ID
                username='dev_test',
                email='dev_test@test.com',
                password=bcrypt.generate_password_hash('dev_test').decode('utf-8'),
                firstname='Dev',
                lastname='Test',
                role='dev_test',
                description='For developer testing purposes.'
            )
            db.session.add(test_user)
            db.session.commit()
            print(f'dev_test user created: {test_user}')
        else:
            print('dev_test user already exists.')

        user = User.query.filter_by(username='test').first()
        if not test:
            user = User(
                    id=str(uuid4()),  # Generate a new UUID for the user ID
                    username='test',
                    email='test@test.com',
                    password=bcrypt.generate_password_hash('test').decode('utf-8'),
                    firstname='Test',
                    lastname='User',
                    role='test',
                    description='For developer testing purposes.'
            )
            db.session.add(user)
            db.session.commit()
            print(f'test user created: {user}')
        else:
            print('test user already exists.')

def delete_test_user():
    app = create_app()
    
    with app.app_context():
        # Check users already exist
        dev_test = User.query.filter_by(username='dev_test').first()
        test = User.query.filter_by(username='test').first()
        
        if dev_test:
            db.session.delete(dev_test)
            db.session.commit()
            print('dev_test user deleted.')
        else:
            print('dev_test user does not exist.')
        if test:
            db.session.delete(test)
            db.session.commit()
            print('test user deleted.')
        else:
            print('test user does not exist.')

def add_test():
    if __name__ == '__main__':
        add_test_user()

def delete_test():
    if __name__ == '__main__':
        delete_test_user()

add_test()
