from app import db
from flask_login import UserMixin
from uuid import uuid4

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid4), unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, default=None)
    lastname = db.Column(db.String, default=None)
    role = db.Column(db.String, default='user')
    description = db.Column(db.String, default=None)
    

    def __repr__(self):
        return f'id: {self.id}; username: {self.username}; email: {self.email}; password: {self.password}; role: {self.role}; description: {self.description}'

class Friendship(db.Model):
    __tablename__ = 'friendship'
    
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), primary_key=True, nullable=False)
    friend_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted'), default='pending', nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now, nullable=False)

    def __repr__(self):
        return f'user_id: {self.user_id}; friend_id: {self.friend_id}; status: {self.status}'
    
class Hangout(db.Model):
    __tablename__ = 'hangout'

    hangout_id = db.Column(db.String(36), primary_key=True, default=str(uuid4), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)
    location_id = db.Column(db.String(36), db.ForeignKey('location.location_id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now, nullable=False)
    description = db.Column(db.String, default=None)

    def __repr__(self):
        return f'hangout_id: {self.hangout_id}; '
    
class HangoutAttendee(db.Model):
    __tablename__ = 'hangout_attendee'

    hangout_attendee_id = db.Column(db.String(36), primary_key=True, default=str(uuid4), unique=True, nullable=False)
    hangout_id = db.Column(db.String(36), db.ForeignKey('hangout.hangout_id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), default='pending', nullable=False)


class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.String(36), primary_key=True, default=str(uuid4), unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)