import os
from sqlalchemy.orm import relationship
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "users"
    # __table_args__ = (db.UniqueConstraint('name'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)
    channels = relationship("Channel", secondary="tags")
    messages = db.relationship("Message", backref="users", lazy=True)
class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False,unique=True)
    users = relationship("User", secondary="tags")
class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    user = relationship(User, backref=backref("tags", cascade="all, delete-orphan"))
    channel = relationship(Channel, backref=backref("tags", cascade="all, delete-orphan"))
    comments = db.relationship("Message", backref="channels", lazy=True)
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user = db.Column(db.String,db.ForeignKey("users.name"),nullable=False)
    channel = db.Column(db.String,db.ForeignKey("channels.title"),nullable=False)