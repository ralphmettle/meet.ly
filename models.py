from app import db
from flask_login import UserMixin
from uuid import uuid4

def generate_uuid():
    return str(uuid4())

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid(), unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, default=None)
    lastname = db.Column(db.String, default=None)
    profile_picture = db.Column(db.String(500), default=None)
    role = db.Column(db.String, default='user')
    welcomed = db.Column(db.Boolean, default=False)
    description = db.Column(db.String, default=None)
    verified = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'id: {self.id}; username: {self.username}; email: {self.email}; password: {self.password}; role: {self.role}; description: {self.description}'

class Friendship(db.Model):
    __tablename__ = 'friendship'
    
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True, nullable=False)
    friend_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True, nullable=False)
    status = db.Column(db.Enum('pending', 'accepted'), default='pending', nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now, nullable=False)

    def __repr__(self):
        return f'user_id: {self.user_id}; friend_id: {self.friend_id}; status: {self.status}'

class Hangout(db.Model):
    __tablename__ = 'hangout'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid(), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.String(36), db.ForeignKey('venue_location.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, default=None)

    def __repr__(self):
        return f'id: {self.id};'
    
class HangoutAttendee(db.Model):
    __tablename__ = 'hangout_attendee'

    hangout_attendee_id = db.Column(db.String(36), primary_key=True, default=generate_uuid(), unique=True, nullable=False)
    id = db.Column(db.String(36), db.ForeignKey('hangout.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), default='pending', nullable=False)

class UserLocation(db.Model):
    __tablename__ = 'user_location'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid(), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref='location', lazy=True)
    name = db.Column(db.String, default='location', nullable=False)

    def __repr__(self):
        return f'id: {self.id}; user_id: {self.user_id}; latitude: {self.latitude}; longitude: {self.longitude}, name: {self.name}'

class VenueLocation(db.Model):
    __tablename__ = 'venue_location'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid(), unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)