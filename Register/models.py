import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "Users"
    # __table_args__ = (db.UniqueConstraint('name'),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,unique=True)
    password = db.Column(db.String, nullable=False)
    blogs = db.relationship("Blog", backref="Users", lazy=True)
    comments = db.relationship("Comment", backref="Users", lazy=True)
    def add_blog(self, title, date):
        b = Blog(title=title, users=self.name,date=date)
        db.session.add(b)
        db.session.commit()

class Blog(db.Model):
    __tablename__ = "Blogs"
    __table_args__ = (db.UniqueConstraint('title'),)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False,unique=True)
    content = db.Column(db.String, nullable=False)
    ratings_count = db.Column(db.Integer, nullable=True)
    date = db.Column(db.String,nullable=False)
    Author = db.Column(db.String,db.ForeignKey("Users.name"),nullable=False)
    comments = db.relationship("Comment", backref="Blogs", lazy=True)
    def add_comment(self,content):
        c = Comment(content)
        db.session.add(c)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True)
    user = db.Column(db.String,db.ForeignKey("Users.name"),nullable=False)
    blog = db.Column(db.String,db.ForeignKey("Blogs.title"),nullable=False)
    
