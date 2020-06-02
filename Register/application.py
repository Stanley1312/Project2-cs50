from flask import Flask, render_template, jsonify, request,session,redirect,url_for
from models import *
import os

PEOPLE_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = r"postgres://qgorardefomjqz:ebcb07859a907fe7ab36b6738c6e8f4d475e6a5457a4d9c8be656c9350b45e29@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d2metr5n3omthh"
app.config["SQLALCHEMY_DATABASE_URI"] = r"postgresql://postgres:1@localhost:5432/project2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.secret_key = "abc"  
db.init_app(app)
list_drone = [] 

def main():
    db.create_all()

@app.route("/")
def home():
    if 'username' in session:
        name = session['username']
        all_channels = Channel.query.all()
        print(all_channels)
        print(type(all_channels))
        if len(all_channels) > 0:
            message = True
        else:
            message = False
        print(message)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'first.jpg')
        return render_template("home.html",user_image=full_filename,name=name,message=message,all_channels=all_channels)
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def register():
    """Register."""
    # Get form information.
    name = request.form.get("name")
    password = request.form.get("password")

    # Add user
    if User.query.filter_by(name=name).first() is None:
        new_user = User(name=name,password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html")
    else:
        return render_template("error.html", message="The name has already existed.")

@app.route("/home", methods=["POST"])
def login():
    """Login."""
    # Get form informationg
    name = request.form.get("name")
    password = request.form.get("password")
    session['username']= name
    # Add user
    if User.query.filter_by(name=name,password=password).first() is None:
        return render_template("register.html")
    else:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'first.jpg')
        return render_template("home.html",user_image=full_filename,name=name)

@app.route("/register")
def turn_back_toregister():
    return render_template("register.html")

@app.route("/home")
def logout():
    session.pop('username', None)
    return render_template("login.html")

@app.route("/channel")
def channel_of_username():
    name = session['username']
    # user = User.query.filter_by(name=name)
    channels = User.query.filter_by(name=name).first().channels
    print(1111111111111111111111111)
    print(type(channels))
    print(len(channels))
    if len(channels) > 0:
        message = True
    else:
        message = False
    return render_template("channel_of_user.html",channels=channels,message=message)

@app.route("/channel",methods=["POST"])
def create_channel():
    name = session['username']
    user = User.query.filter_by(name=name)[0]
    id_user = user.id
    title = request.form.get("title")
    new_channel = Channel(title=title,creator_id=id_user)
    user.channels.append(new_channel)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('channel_of_username'))

@app.route("/channel/infor/<string:title>")
def channelRender(title):
    channel = Channel.query.filter_by(title=title).all()[0]
    title = channel.title
    users = channel.users

    return render_template("channel_info.html",title=title,users=users)

if __name__ == "__main__":
    with app.app_context():
        main()