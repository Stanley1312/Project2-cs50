from flask import Flask, render_template, jsonify, request,session,redirect,url_for
from models import *
from flask_socketio import SocketIO, join_room, leave_room
import os

#duong link anh
PEOPLE_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = r"postgres://qgorardefomjqz:ebcb07859a907fe7ab36b6738c6e8f4d475e6a5457a4d9c8be656c9350b45e29@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d2metr5n3omthh"
app.config["SQLALCHEMY_DATABASE_URI"] = r"postgresql://postgres:1@localhost:5432/project2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.secret_key = "abc"  
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
db.init_app(app)
socketio = SocketIO(app)
list_drone = [] 
title_name = []



def main():
    #tao database
    db.create_all()

@app.route("/")
def home():
    #check người dùng còn ở trong channel hay không 
    if 'channel' in session :
        title = session['channel']
        return redirect(url_for('channel_detail',title=title))
    #check nguoi dung con dang nhap hay khong
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

    name = request.form.get("name")
    password = request.form.get("password")
    
    session['username']= name
    if User.query.filter_by(name=name,password=password).first() is None:

        return render_template("register.html")
    else:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'first.jpg')
        return render_template("home.html",user_image=full_filename,name=name)

@app.route("/register")
def turn_back_toregister():
    return render_template("register.html")
@app.route("/goback")
def goback():
    if 'channel' in session :
        session.pop('channel',None)
    return redirect(url_for('channel'))
@app.route("/home")
def logout():
    session.pop('username', None)
    return render_template("login.html")
@app.route("/channel",methods=["POST","GET"])
def channel():
    #Danh sach cac channel hien co 
    alert = False
    name = session['username']    
    if request.method == "POST":
        channelname = request.form.get('channelname')
        print('--------------channelname----------')
        print(channelname)
        #them channel moi 
        add_channel = Channel.query.filter_by(title=channelname).first()
        if add_channel is None:
            user = User.query.filter_by(name=name)[0]
            new_channel = Channel(title=channelname)
            user.channels.append(new_channel)
            db.session.add(new_channel)
            db.session.commit()
        else:
            #cach bao neu ten channel da ton tai
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
@app.route("/channel_detail/<string:title>")
def channel_detail(title):
    #Noi dung cua channel
    name = session['username']  
    session['channel'] = title
    return render_template("session.html",title=title,username=name)

def messageReceived():
    print('message was received!!!')

@socketio.on('my notice')
def notice(json):
    #ham canh bao khi moi ket noi vao socket
    print('received my event: ' + str(json))
    title = json.get('title')
    #get tin nhan hien co tu database ve
    mess_data = Message.query.filter_by(channel=title).all()
    print("------------messdata------------")
    print(mess_data)
    for mess in mess_data:
        username = mess.user
        messages = mess.content
        id = mess.id
        data = {"user_name" : username,
                "message" : messages,
                "id" : id
                }
        #show tin nhan qua html thong qua socket
        socketio.emit('my response', data, callback=messageReceived)
@socketio.on('join')
def on_join(data):
    # ham join channel
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.send(username + ' has entered the room.', room=room)
    print(username + 'has entered the room '+ room)
@socketio.on('leave')
def on_leave(data):
    #ham thoat khoi channel
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.send(username + ' has left the room.', room=room)
    print(username + 'has LEFT the room '+ room)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received my event: ' + str(json))
    # print(type(json))
    print(json.get('user_name'))
    print(json.get('message'))
    print("-TITLE------------------")
    print(json.get('title'))
    user_name = json.get('user_name')
    content = json.get('message')
    title = json.get('title')
    #lay tat ca tin nhan hien co ve
    mess_data = Message.query.filter_by(channel=title).all()
    #kiem tra neu co hon 100 tin nhan se xoa tin nhan cuoi cung
    if len(mess_data) > 100:
        mess_data = mess_data.pop(100)
    #them tin nhan moi nhat vao database
    message = Message(content=content,user=user_name,channel=title)
    db.session.add(message)
    db.session.commit()
    mess_data = Message.query.filter_by(channel=title).all()
    print("------------messdata------------")
    print(mess_data)
    for mess in mess_data:
        username = mess.user
        messages = mess.content
        id = mess.id
        data = {"user_name" : username,
                "message" : messages,
                "id" : id
                }
    socketio.emit('my response', data, callback=messageReceived,room=title,broadcast=True)
@socketio.on('delete')
def delete_content(data):
    print('Receive deleted data ' + str(data))
    start = "-"
    end = "X"
    #lay thong tin ve tin nhan bi xoa
    data = data.get('data')
    #lay content cua tin nhan
    data = ((data.split(start))[1].split(end)[0])
    print(data)
    #xoa tin nhan tren database
    Message.query.filter_by(id=data).delete()
    db.session.commit()
    print('---------DELETED------------')
if __name__ == "__main__":
    socketio.run(app, debug=True)
    with app.app_context():
        main()
