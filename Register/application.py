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
title_name = []


def main():
    db.create_all()

@app.route("/")
def home():
    if 'username' in session:
        print("---------singin----------")
        print(session['username'])
        name = session['username']
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'first.jpg')
        return render_template("home.html",user_image=full_filename,name=name)
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def register():
    """Register."""
    # Get form information.
    name = request.form.get("name")
    password = request.form.get("password")
    print("--------------NAME------------")
    print(name)

    result = User.query.filter_by(name=name).first()
    print("-----------------RESULT------------")
    # Add user
    if result is None:
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
    # displayname  = request.args.get("displayname")
    name = request.form.get("name")
    password = request.form.get("password")
    # print("---davaoroi-----")
    
    session['username']= name
    # if 'username' in session:
    #     user = session['username']
    #     print(user)
    # print("adfadfkasndfoasdnfasdf")
    # # Add use
    
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
@app.route("/channel",methods=["POST","GET"])
def channel():
    alert = False
    name = session['username']    
    if request.method == "POST":
        channelname = request.form.get('channelname')
        print('--------------channelname----------')
        add_channel = Channel.query.filter_by(title=channelname).first()
        if add_channel is None:
            user = User.query.filter_by(name=name)[0]
            new_channel = Channel(title=channelname)
            user.channels.append(new_channel)
            db.session.add(new_channel)
            db.session.commit()
        else:
            alert = True
    list_channel = Channel.query.all()
    if len(list_channel)> 0 :
        print('-------vo roi ne --------')
        message = True
    else : 
        print('-------vo roi ne  hai --------')
        message  = False
    print("------------listchannel---------------")
    print(list_channel)
    print(message)
    return render_template("channel.html",alert=alert,channel=list_channel,message=message)
@app.route("/channel_detail")
def channel_detail():
    



if __name__ == "__main__":
    with app.app_context():
        main()