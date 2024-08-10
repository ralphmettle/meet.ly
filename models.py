from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, default=None)
    lastname = db.Column(db.String, default=None)
    profile_picture = db.Column(db.String(500), default=None)

    role = db.Column(db.String, default='user')
    welcomed = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)

    description = db.Column(db.String, default=None)

    #friends = db.relationship('Friendship', backref='user', lazy=True) 
    
    sent_friend_requests = db.relationship('Friendship', 
                                           foreign_keys='Friendship.sender_id', 
                                           backref='sender', 
                                           lazy=True)
    
    received_friend_requests = db.relationship('Friendship', 
                                               foreign_keys='Friendship.recipient_id', 
                                               backref='recipient', 
                                               lazy=True)
    
    def __repr__(self): 
        return f'id: {self.id}; username: {self.username}; email: {self.email}; password: {self.password}; role: {self.role}; description: {self.description}'

class Friendship(db.Model):
    __tablename__ = 'friendship'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    accepted = db.Column(db.Boolean, default=False, nullable=False)
    pending = db.Column(db.Boolean, default=True, nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.now, nullable=False)

    def __repr__(self):
        return f'user_id: {self.user_id}; friend_id: {self.friend_id}; status: {self.status}'

class Hangout(db.Model):
    __tablename__ = 'hangout'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_creator = db.Column(db.Boolean, default=False, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('venue_location.id'), nullable=False) 
    name = db.Column(db.String, nullable=False)

    description = db.Column(db.String, default=None)
    date_created = db.Column(db.DateTime, default=db.func.now, nullable=False)

    def __repr__(self):
        return f'id: {self.id};'
    
class HangoutAttendee(db.Model):
    __tablename__ = 'hangout_attendee'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    hangout_id = db.Column(db.Integer, db.ForeignKey('hangout.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), default='pending', nullable=False)

class UserLocation(db.Model):
    __tablename__ = 'user_location'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='location', lazy=True)
    name = db.Column(db.String, default='location', nullable=False)

    def __repr__(self):
        return f'id: {self.id}; user_id: {self.user_id}; latitude: {self.latitude}; longitude: {self.longitude}, name: {self.name}'

class VenueLocation(db.Model):
    __tablename__ = 'venue_location'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)