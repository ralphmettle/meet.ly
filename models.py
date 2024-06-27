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

'''  
class Friends(db.Model):
    __tablename__= 'friends'

    user_id = db.Column(db.String(36), foreign_key=True)
    friend_id = db.Column(db.String(36), forign_key=True)
'''