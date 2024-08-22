from app import create_app, db
from models import User, UserLocation, Friendship
from flask_bcrypt import Bcrypt

def add_test_user():
    app = create_app()
    bcrypt = Bcrypt(app)
    
    with app.app_context():        
        # Check if the user already exists
        test = User.query.filter_by(username='dev_test').first()
        if not test:
            # Create the test user
            dev_test_user = User(
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

def test_friendships():
    app = create_app()

    with app.app_context():
        johndoe = User.query.filter_by(username='johndoe').first()
        janedoe = User.query.filter_by(username='janedoe').first()
        timsmith = User.query.filter_by(username='timsmith').first()
        tinasmith = User.query.filter_by(username='tinasmith').first()

        friendships = [
            (johndoe, janedoe),
            (johndoe, timsmith),
            (johndoe, tinasmith),
            (janedoe, timsmith),
            (janedoe, tinasmith),
            (timsmith, tinasmith),
        ]

        for friendship in friendships:
            check_friendship = Friendship.query.filter_by(
                user_id=friendship[0].id,
                friend_id=friendship[1].id
            ).first()
            if not check_friendship:
                new_friendship = Friendship(
                    user_id=friendship[0].id,
                    friend_id=friendship[1].id
                )
                db.session.add(new_friendship)
                db.session.commit()
                print(f'Friendship between {friendship[0].username} and {friendship[1].username} created.')
            else:
                print(f'Friendship between {friendship[0].username} and {friendship[1].username} already exists.')

def delete__test_friendships():
    app = create_app()

    with app.app_context():
        friendships = Friendship.query.all()
        if friendships:
            for friendship in friendships:
                db.session.delete(friendship)
            db.session.commit()
            print('Friendships deleted.')
        else:
            print('Friendships do not exist.')

def test_user_friendships():
    app = create_app()

    with app.app_context():
        test = User.query.filter_by(username='test').first()
        johndoe = User.query.filter_by(username='johndoe').first()
        janedoe = User.query.filter_by(username='janedoe').first()

        friendships = [
            (test, johndoe),
            (test, janedoe),
        ]

        for friendship in friendships:
            check_friendship = Friendship.query.filter_by(
                user_id=friendship[0].id,
                friend_id=friendship[1].id
            ).first()
            if not check_friendship:
                new_friendship = Friendship(
                    user_id=friendship[0].id,
                    friend_id=friendship[1].id,
                    accepted=True
                )
                db.session.add(new_friendship)
                db.session.commit()
                print(f'Friendship between {friendship[0].username} and {friendship[1].username} created.')
            else:
                print(f'Friendship between {friendship[0].username} and {friendship[1].username} already exists.')

def get_user_friends(user_id):
    app = create_app()

    with app.app_context():
        user = db.session.get(User, user_id)
        
        if user:
            friends = user.friends + user.friend_of

            if not friends:
                return {'error': 'User has no friends.'}

            friends_list = [{'id': friend.id, 'username': friend.username} for friend in friends]
            return friends_list
        else:
            return {'error': 'User not found'}
        
def get_user_friend_requests(user_id):
    app = create_app()

    with app.app_context():
        user = db.session.get(User, user_id)
        
        if user:
            friend_requests = user.friend_requests

            if not friend_requests:
                return {'error': 'User has no friend requests.'}

            friend_requests_list = [{'id': friend.id, 'username': friend.username} for friend in friend_requests]
            return friend_requests_list
        else:
            return {'error': 'User not found'}
        
def get_user_sent_requests(user_id):
    app = create_app()

    with app.app_context():
        user = db.session.get(User, user_id)
        
        if user:
            sent_requests = user.sent_requests

            if not sent_requests:
                return {'error': 'User has not sent any friend requests.'}

            sent_requests_list = [{'id': friend.id, 'username': friend.username} for friend in sent_requests]
            return sent_requests_list
        else:
            return {'error': 'User not found'}

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

def add_friendships():
    if __name__ == '__main__':
        test_friendships()

def delete_friendships():
    if __name__ == '__main__':
        delete__test_friendships()

def add_test_friends():
    if __name__ == '__main__':
        test_user_friendships()

def get_friends(num):
    if __name__ == '__main__':
        print('User friends:')
        print(get_user_friends(num))
        print('User friend requests:')
        print(get_user_friend_requests(num))
        print('User sent requests:')
        print(get_user_sent_requests(num))

# Initialise the database for testing purposes.
def init_db():
    add_test()
    add_dummy()
    add_friendships()
    add_test_friends()

def delete_db():
    delete_test()
    delete_dummy()
    delete_friendships()

# Run the following to initialise the database for testing purposes.
# init_db()