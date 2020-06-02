import os
from sqlalchemy.orm import relationship, backref
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


Tag = db.Table('link_channel_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'))
)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)
    channels = db.relationship("Channel", secondary=Tag)
    messages = db.relationship("Message", backref="users", lazy=True)

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False,unique=True)
    creator_id =db.Column(db.Integer, nullable=False)
    messages = db.relationship("Message", backref="channels", lazy=True)
    users= db.relationship("User",secondary=Tag)

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user = db.Column(db.String,db.ForeignKey("users.name"),nullable=False)
    channel = db.Column(db.String,db.ForeignKey("channels.title"),nullable=False)