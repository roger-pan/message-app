from datetime import datetime
from . import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint, func
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash



class User(UserMixin, db.Model):
    """Data model for Users"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username  = Column(String(64), index=True, unique=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    salt = Column(String(64))
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now())
    image = Column(String(200))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_dict(dict):

        return users(
            id =dict['id'],
            username=dict['username'],
            first_name=dict['first_name'],
            last_name =dict['last_name'],
            email=dict['email'],
            password_hash=dict['password_hash'], 
            salt=dict['salt'],
            created_at=dict['created_at'],
            updated_at=dict['updated_at'],
            icon = dict['image']  

            )

    def to_dict(self):
       """Return object data in easily serializable format"""
       return {
            'id'  : self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email':self.email,
            'password_hash':self.password_hash,
            'salf':self.salt,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'image': self.image
       }


class Chat(db.Model):
    """ Data Model for Conversations"""

    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now())

    @staticmethod
    def from_dict(dict):
        return Chat(
            name =dict['name'],
            created_at = datetime.utcnow(),
        )
    
    def to_dict(self):

        return {
            'id' : self.id,
            'name': self.name,
            'created_at': self.created_at,
        }


class ChatUser(db.Model):
    """ Data Model for lookup between groups and users"""

    __tablename__ = "chat_users"
    __tableargs__ = (PrimaryKeyConstraint('user_id', 'chat_id'),
    )

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), primary_key=True)

    @staticmethod
    def from_dict(dict, user_id):

        return ChatUser(
            user_id =user_id,
            chat_id =dict['chat_id']
        )

    def to_dict(self):

        return {
            'user_id': self.user_id,
            'chat_id': self.chat_id
        }


class Message(db.Model):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    @staticmethod
    def from_dict(dict, chat_id, user_id):

        return Message(
            sender_id = dict['sender_id'],
            content =dict['content'],
            chat_id = int(chat_id),
            created_at = dict['created_at'],
        )
    
    def to_dict(self):

        return {
        'id': self.id,
        'chat_id': self.chat_id,
        'sender_id': self.sender_id,
        'content': self.content,
        'created_at': self.created_at,
        }