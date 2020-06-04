from flask import Flask, render_template, jsonify, request,session,redirect,url_for
from models import *
from sqlalchemy import and_
import os

PEOPLE_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = r"postgres://qgorardefomjqz:ebcb07859a907fe7ab36b6738c6e8f4d475e6a5457a4d9c8be656c9350b45e29@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d2metr5n3omthh"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1@localhost:5432/postgres"
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
        if len(all_channels) > 0:
            message = True
        else:
            message = False
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'first.jpg')

        users = User.query.all()
        #Get list of requests sent to current user
        user = User.query.filter_by(name=name).first()
        receive_requests = Invitation.query.filter(and_(Invitation.end_user_id==user.id, Invitation.flag_active==True)).all()
        list_user_sent = []
        for receive_request in receive_requests:
            for user in users:
                for channel in all_channels:
                    if user.id == receive_request.start_user_id and channel.id == receive_request.channel_id:
                        list_user_sent.append((user.name, channel.title, receive_request))

        return render_template("home.html", user_image=full_filename, name=name, message=message, all_channels=all_channels, list_user_sent=list_user_sent)
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
    users = channel.users

    return render_template("channel_info.html",channel=channel,users=users)

@app.route("/send_request/<string:flag>", methods=['POST'])
def send_request(flag):
    name = session['username']
    user_start = User.query.filter_by(name=name).first()
    start_user_id = user_start.id
    channel_id = request.form.get('channel_id')
    channel = Channel.query.filter_by(id=channel_id).first()
    if flag == '1':
        end_user_id = channel.creator_id

        #Add request to db
        request_join = Invitation(start_user_id=start_user_id, end_user_id=end_user_id, channel_id=channel_id, flag_active=True, flag_direction=False)
        db.session.add(request_join)
        db.session.commit()
    elif flag == '0':
        user_end = User.query.filter_by(name=request.form.get('user_name')).first()
        request_join = Invitation(start_user_id=start_user_id, end_user_id=user_end.id, channel_id=channel_id, flag_active=True, flag_direction=True)
        db.session.add(request_join)
        db.session.commit()
    return redirect(url_for('channelRender', title=channel.title))

@app.route('/add_user/<string:flag>/<string:channel_title>/<string:user_name>/<int:request_id>')
def add_user_or_not(flag, channel_title, user_name, request_id):
    request_confirm = Invitation.query.get(request_id)
    name = session['username']
    if flag == '0':
        if request_confirm.flag_direction:
            user = User.query.filter_by(name=name).first()
        else:
            user = User.query.filter_by(name=user_name).first()
        channel = Channel.query.filter_by(title=channel_title).first()
        channel.users.append(user)
        db.session.add(channel)
        db.session.commit()
    request_confirm.flag_active=False
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    with app.app_context():
        main()