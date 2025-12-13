#data_structures.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)
                         
    def set_password(self, password):
        self.password = password
    def check_password(self, password):
        return self.password == password
    
    def __repr(self):
        return '<User %r>' % self.id

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    release_year = db.Column(db.Integer)

    reviews = db.relationship("Review", backref="show")

    def __repr__(self):
      return f"<Show {self.title}>"
    
class Episode(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
  episode_number = db.Column(db.Integer, nullable=False)
  title = db.Column(db.String(100))

  show = db.relationship("Show", backref="episodes")
  watched = db.relationship("Watched", backref="episode")

  def __repr__(self):
    return f"<Episode {self.episode_number}>"
  
class Watched(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"), nullable=False)
  watched = db.Column(db.Boolean, default=True)

  __table_args__ = (
    db.UniqueConstraint("user_id", "episode_id", name="user_watched_episode"),
  )


  def __repr__(self):
    return f"<Watched user={self.user_id} episode={self.episode_id}>"
  
class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  show_id = db.Column(db.Integer, db.ForeignKey("show.id"), nullable=False)
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