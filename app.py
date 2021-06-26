"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'i-have-a-secret'


connect_db(app)
db.create_all()

@app.route("/users")
def list_users():
    """List users and show add form."""

    #users = User.query.order_by(User.first_name, User.last_name, User.image_url).all()
    users = User.query.all()
    return render_template("users.html", users = users)

@app.route("/users", methods=["POST"])
def form_users():
    #list users and show add form.
    new_user = User(first_name = request.form["first_name"], last_name = request.form["last_name"], image_url = request.form["image_url"])
    db.session.add(new_user)
    db.session.commit()
    print(new_user.full_name)
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get(user_id)
    posts = user.posts
    return render_template("userdetail.html", user = user, posts = posts)

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def edit(user_id):
    user = User.query.get(user_id)
    return render_template("edit.html", user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])    
def edit_form(user_id):
    #list users and show add form.
    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/<int:post_id>')
def show_post(user_id, post_id):
    user = User.query.get(user_id)
    posts = Post.query.get(post_id)
    return render_template("postdetail.html", posts = posts, user = user)

@app.route('/users/<int:user_id>/newpost')
def new_post(user_id):
    user = User.query.get(user_id)
    return render_template("postcreate.html", user = user)

@app.route('/users/<int:user_id>/newpost',methods=["POST"])
def create_post(user_id):
    user = User.query.get(user_id)
    new_post = Post(title = request.form["title"], content = request.form["content"], user_id = user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect("/users")





