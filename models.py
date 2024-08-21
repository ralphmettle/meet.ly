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

    friends = db.relationship(
        'User',
        secondary='friendship',
        primaryjoin='and_(User.id==Friendship.user_id, Friendship.accepted==True)',
        secondaryjoin='and_(User.id==Friendship.friend_id, Friendship.accepted==True)',
        backref='friend_of',
        viewonly=True
    )

    friend_requests = db.relationship(
        'User',
        secondary='friendship',
        primaryjoin='and_(User.id==Friendship.friend_id, Friendship.accepted==False)',
        secondaryjoin='and_(User.id==Friendship.user_id, Friendship.accepted==False)',
        backref='sent_requests',
        viewonly=True
    )
    
    def __repr__(self): 
        return f'id: {self.id}; username: {self.username}; email: {self.email}; password: {self.password}; role: {self.role}; description: {self.description}'

class Friendship(db.Model):
    __tablename__ = 'friendship'
    
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    accepted = db.Column(db.Boolean, default=False, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    def __repr__(self):
        return f'id: {self.id}; user_id: {self.user_id}; friend_id: {self.friend_id}; accepted: {self.accepted}'

class Hangout(db.Model):
    __tablename__ = 'hangout'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_creator = db.Column(db.Boolean, default=False, nullable=False)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    place_name = db.Column(db.String, nullable=False)
    place_address = db.Column(db.String, nullable=False)
    place_review_summary = db.Column(db.String, nullable=True)
    place_id = db.Column(db.String, nullable=False)
    place_photo_url = db.Column(db.String, nullable=True)
    place_maps_link = db.Column(db.String, nullable=False)

    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    date_created = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    attendees = db.relationship('HangoutAttendee', back_populates='hangout')
    memories = db.relationship('Memory', back_populates='hangout')
    
    def __repr__(self):
        return f'id: {self.id};'
    
class HangoutAttendee(db.Model):
    __tablename__ = 'hangout_attendee'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    hangout_id = db.Column(db.Integer, db.ForeignKey('hangout.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), default='pending', nullable=False)

    hangout = db.relationship('Hangout', back_populates='attendees', lazy=True)
    user = db.relationship('User', backref='hangouts', lazy=True)

class Memory(db.Model):
    __tablename__ = 'memory'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hangout_id = db.Column(db.Integer, db.ForeignKey('hangout.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    hangout = db.relationship('Hangout', back_populates='memories')

class MemoryData(db.Model):
    __tablename__ = 'memory_data'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    memory_id = db.Column(db.Integer, db.ForeignKey('memory.id'), nullable=False)
    image = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=True)
    
    memory = db.relationship('Memory', backref='data')

class UserLocation(db.Model):
    __tablename__ = 'user_location'

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    name = db.Column(db.String, default='location', nullable=False)

    user = db.relationship('User', backref='location')  

    def __repr__(self):
        return f'id: {self.id}; user_id: {self.user_id}; latitude: {self.latitude}; longitude: {self.longitude}, name: {self.name}'