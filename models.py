"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime
db = SQLAlchemy()

DEFAULT_IMAGE_URL ="https://tinyurl.com/y3rfozh8"


def connect_db(app):
    db.app = app
    db.init_app(app)
    
class User(db.Model): 
    __tablename__ = "users"
    id = db.Column(db.Integer, 
        primary_key=True)
    first_name = db.Column(db.Text, 
        nullable=False)
    last_name = db.Column(db.Text, 
        nullable=False)
    image_url = db.Column(db.Text, 
        nullable=False, default = DEFAULT_IMAGE_URL)
    posts = db.relationship('Post')
    @property
    def full_name(self):
        u = self
        return f"<User {u.first_name} {u.last_name} {u.image_url}>"

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, 
        primary_key=True)
    title = db.Column(db.Text, 
        nullable=False)
    content = db.Column(db.Text, 
        nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, 
        db.ForeignKey('users.id'))
    curr_user = db.relationship('User')


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from app import app

    connect_db(app)

    db.drop_all()
    db.create_all()
    example_data()