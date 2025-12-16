#data_structures.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)
                         
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        if self.password and not self.password.startswith(("pbkdf2:", "scrypt:", "argon2:")):
            if self.password == password:
                self.set_password(password)
                db.session.commit()
                return True
            return False
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User %r>' % self.id

class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    cover = db.Column(db.Text)
    director = db.Column(db.String(255))
    cast = db.Column(db.Text)
    release_year = db.Column(db.Integer)
    rating = db.Column(db.String(20))
    seasons = db.Column(db.String(20))
    genres = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Show {self.title}>"
    
class Episode(db.Model):
  __tablename__ = "episodes"

  id = db.Column(db.Integer, primary_key=True)
  show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), nullable=False)
  episode_number = db.Column(db.Integer, nullable=False)

  show = db.relationship("Show", backref="episodes")
  watched = db.relationship("Watched", backref="episode")

  def __repr__(self):
    return f"<Episode {self.episode_number}>"
  
class Watched(db.Model):
  __tablename__ = "watched"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"), nullable=False)
  watched = db.Column(db.Boolean, default=True)

  __table_args__ = (
    db.UniqueConstraint("user_id", "episode_id", name="user_watched_episode"),
  )


  def __repr__(self):
    return f"<Watched user={self.user_id} episode={self.episode_id}>"
  
class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), nullable=False)
  rating = db.Column(db.Integer)  # 1–5
  review_text = db.Column(db.Text)

  __table_args__ = (
    db.UniqueConstraint("user_id", "show_id", name="user_review"),
  )

  def __repr__(self):
    return f"<Review user={self.user_id} show={self.show_id}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class WatchStatus(db.Model):
    __tablename__ = "watch_status"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), primary_key=True)
    status = db.Column(db.String(20), nullable=False)

class List(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=True)
    
    items = db.relationship("ListItem", backref="list", cascade="all, delete-orphan")

class ListItem(db.Model):
    __tablename__ = "list_items"
    list_id = db.Column(db.Integer, db.ForeignKey("lists.id"), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey("shows.id"), primary_key=True)
    position = db.Column(db.Integer)


