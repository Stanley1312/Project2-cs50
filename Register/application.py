from flask import Flask, render_template, jsonify, request,session,redirect,url_for
from models import *
import os

PEOPLE_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = r"postgres://qgorardefomjqz:ebcb07859a907fe7ab36b6738c6e8f4d475e6a5457a4d9c8be656c9350b45e29@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d2metr5n3omthh"
app.config["SQLALCHEMY_DATABASE_URI"] = r"postgresql://postgres:1@localhost:5432/project1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.secret_key = "abc"  
db.init_app(app)
list_drone = [] 

def main():
    db.create_all()

@app.route("/")
def home():
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
    # Get form information.
    name = request.form.get("name")
    password = request.form.get("password")

    session['username'] = name
    # if 'username' in session:
    #     user = session['username']
    #     print(user)
    # print("adfadfkasndfoasdnfasdf")
    # # Add user
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

@app.route('/home2',methods=["POST"])
def searching():
    selection = request.form.get("selection")
    search = request.form.get("search")
    # print(selection)
    # print(search)
    message = True
    if selection == "Users":
        results = Blog.query.filter_by(Author=search).all()
    elif selection == "Rating":
        results = Blog.query.filter_by(ratings_count=search).all()
    elif selection == "Title":
        results = Blog.query.filter_by(title=search).all()
    elif selection == "Date":
        results = Blog.query.filter_by(date=search).all() 
    if results == []:
        message = False
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'first.jpg')
        return render_template("home.html",user_image=full_filename,message=message)
    
    return render_template("resultSearching.html",results=results)

@app.route("/blog/<string:title>",methods=["POST","GET"])
def blogRender(title):
    user_name = session['username']
    # title = request.args.get("title")
    if request.method == "GET":
        blog = Blog.query.filter_by(title=title).all()
        author = blog[0].Author
        title = blog[0].title
        content = blog[0].content
        comments=Comment.query.filter_by(blog=title).all()
        print("-----------getcomment------------")
        print(comments)
        message = True
        if len(comments) == 0:
            message = False
        alert = False
        drone = 0
    if request.method == "POST":
        # print("vo duoc roi ne leu leu")
        content_comment = request.form.get("content")
        content_comment = request.form.get("content_comment")
        drone = request.form.get("drone")
        drone = int(drone)
        list_drone.append(drone)
        drone = sum(list_drone)/ len(list_drone)
        # print("--------------title---------------")
        # print(title)
        author = request.form.get("author")
        blog = Blog.query.filter_by(title=title).all()[0]
        print("--------------blog---------------")
        print(blog)
        content = blog.content
        print("--------------content---------------")
        print(content)
        comments=Comment.query.filter_by(blog=title).all()
        print("--------------comment---------------")
        print(comments)
        message = True
        check_comment = Comment.query.filter_by(user=user_name).all()
        print("--------------check-content---------------")
        print(check_comment)
        if len(check_comment)>0:
            alert = True
        else:
            print(88888888)
            new_comment = Comment(blog=title,content=content_comment,user=user_name)
            db.session.add(new_comment)
            db.session.commit()
            alert = False
        comments = Comment.query.filter_by(user=user_name).all()
        print(alert)   # return redirect(url_for('blogRender',title=title))
    return render_template("blog.html",title=title,content=content,author=author,comments=comments,message=message,alert=alert,drone=drone)
@app.route("/blog/<int:id>",methods=["GET"])
def blog_api(id):
    """Return details about a single flight."""

    # Make sure blog exists.
    blog = Blog.query.get(id)
    print("khoa oc choooooooooooooooooooooooooooooooooooo")
    print(blog)
    print(type(blog))
    if blog is None:
        return jsonify({"error": "Invalid blog"}), 404

    # Get all passengers.
    comments = blog.comments
    names = []
    for comment in comments:
        names.append(comment.content)
    return jsonify({  
            "Author": blog.Author,
            "Title": blog.title,
            "Comment": names
        })


if __name__ == "__main__":
    with app.app_context():
        main()