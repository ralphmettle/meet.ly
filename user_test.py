from app import create_app, db
from models import User, UserLocation
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
            dev_test_user = User(
                id=str(uuid4()),  # Generate a new UUID for the user ID
                username='dev_test',
                email='dev_test@test.com',
                password=bcrypt.generate_password_hash('dev_test').decode('utf-8'),
                firstname='Dev',
                lastname='Test',
                role='dev_test',
                description='For developer testing purposes.',
                welcomed=True,
                verified=True
            )
            db.session.add(dev_test_user)
            db.session.commit()
            print(f'dev_test user created: {dev_test_user}')
        else:
            print('dev_test user already exists.')

        user = User.query.filter_by(username='test').first()
        if not user:
            user = User(
                    id=str(uuid4()),  # Generate a new UUID for the user ID
                    username='test',
                    email='test@test.com',
                    password=bcrypt.generate_password_hash('test').decode('utf-8'),
                    firstname='Test',
                    lastname='User',
                    role='test',
                    description='For developer testing purposes.',
                    welcomed=False,
                    verified=True
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

def add_dummy_users():
    app = create_app()
    bcrypt = Bcrypt(app)
    
    with app.app_context():        
        dummy_users = {
            'johndoe': ['John', 'Doe'],
            'janedoe': ['Jane', 'Doe'],
            'timsmith': ['Tim', 'Smith'],
            'tinasmith': ['Tina', 'Smith'],
        }

        dummy_locations = [
            [51.5074, -0.1278],  # Central London
            [51.5154, -0.1410],  # Near Oxford Circus
            [51.5115, -0.1197],  # Covent Garden
            [51.5033, -0.1195],  # Trafalgar Square
        ]

        check_users = User.query.filter(User.username.in_(dummy_users.keys())).all()

        if not check_users:
            for user, names in dummy_users.items():
                dummy = User.query.filter_by(username=user).first()
                if not dummy:
                    dummy_user = User(
                        id=str(uuid4()),
                        username=user,
                        email=f'{user}@test.com',
                        password=bcrypt.generate_password_hash(user).decode('utf-8'),
                        firstname=names[0],
                        lastname=names[1],
                        role='test',
                        description='For developer testing purposes.',
                        welcomed=True,
                        verified=True,
                        profile_picture=f'{user}.jpg'
                    )
                    db.session.add(dummy_user)
                
            db.session.commit()
            print(f'test users created: {dummy_users}')

            for user, location in zip(dummy_users.keys(), dummy_locations):
                user = User.query.filter_by(username=user).first()
                if user:
                    dummy_location = UserLocation(
                        id=str(uuid4()),
                        user_id=user.id,
                        latitude=location[0],
                        longitude=location[1]
                    )
                    db.session.add(dummy_location)
            
            db.session.commit()
            print('test locations created.')
        else:
            print('test users already exist.')

def delete_dummy_users():
    app = create_app()
    
    with app.app_context():
        dummy_users = ['johndoe', 'janedoe', 'timsmith', 'tinasmith']
        
        check_users = User.query.filter(User.username.in_(dummy_users)).all()
        check_user_locations = UserLocation.query.filter(
            UserLocation.user_id.in_([user.id for user in check_users])
            ).all()

        if check_users:
            for user in check_users:
                db.session.delete(user)
            for location in check_user_locations:
                db.session.delete(location)

            db.session.commit()
            print('test users and locations deleted.')
        else:
            print('test users and locations do not exist.')

def test_user_welcome():
    app = create_app()

    with app.app_context():
        test = User.query.filter_by(username='test').first()
        if test:
            if test.welcomed == False:
                test.welcomed = True
                db.session.commit()
                print('test user welcomed.')
            elif test.welcomed == True:
                test.welcomed = False
                db.session.commit()
                print('test user unwelcomed.')
        else:
            print('test user does not exist.')

def add_test():
    if __name__ == '__main__':
        add_test_user()

def delete_test():
    if __name__ == '__main__':
        delete_test_user()

def toggle_welcome():
    if __name__ == '__main__':
        test_user_welcome()

def add_dummy():
    if __name__ == '__main__':
        add_dummy_users()

def delete_dummy():
    if __name__ == '__main__':
        delete_dummy_users()

add_dummy()