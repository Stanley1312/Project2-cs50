import os
from sqlalchemy.orm import relationship,backref
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('users_id',db.Integer,db.ForeignKey('users.id'),primary_key=True),
    db.Column('channels_id',db.Integer,db.ForeignKey('channels.id'),primary_key=True)
    )
class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (db.UniqueConstraint('name'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)
    channels = db.relationship('Channel', secondary=tags,lazy='subquery',backref=db.backref('channels',lazy=True))
    messages = db.relationship("Message", backref="users", lazy=True)

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False,unique=True)
    users = db.relationship("User", secondary=tags)
    messages = db.relationship("Message", backref="channels", lazy=True)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user = db.Column(db.String,db.ForeignKey("users.name"),nullable=False)
    channel = db.Column(db.String,db.ForeignKey("channels.title"),nullable=False)