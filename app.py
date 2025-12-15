import os
from flask import Flask, render_template, jsonify, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from data_structure import db, login_manager, Show, Episode, User, Watched, Review
from routes import auth_bp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def createApp() :
  app = Flask(__name__)
  app.config.update(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(BASE_DIR, 'instance/cse108webtv.db')}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
  )

  db.init_app(app)
  login_manager.init_app(app)
  app.register_blueprint(auth_bp)

    # ------------- PROTECT ADMIN WITH LOGIN + is_admin -------------
  class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
      return current_user.is_authenticated and getattr(current_user, "is_admin", False)

    def inaccessible_callback(self, name, **kwargs):
      return redirect(url_for("auth.login"))

  class SecureModelView(ModelView):
    def is_accessible(self):
      return current_user.is_authenticated and getattr(current_user, "is_admin", False)

    def inaccessible_callback(self, name, **kwargs):
      return redirect(url_for("auth.login"))

  # ------------- FLASK-ADMIN SETUP -------------
  admin = Admin(
    app,
    name="Admin",
    index_view=SecureAdminIndexView(url="/admin")
  )

  # Expose your models in the admin UI
  admin.add_view(SecureModelView(User, db.session))
  admin.add_view(SecureModelView(Show, db.session))
  admin.add_view(SecureModelView(Episode, db.session))
  admin.add_view(SecureModelView(Watched, db.session))
  admin.add_view(SecureModelView(Review, db.session))

  @app.route("/")
  def home():
    return render_template("login.html")

  @app.route("/index")
  @login_required
  def index():
    shows = Show.query.order_by(Show.title).all()
    return render_template("index.html", shows=shows)
  
  @app.route("/show-db")
  def show_db():
    return render_template("showDB.html")
  
  @app.route("/show/<int:show_id>")
  @login_required
  def show_detail(show_id):
    show = Show.query.get_or_404(show_id)

    episodes = Episode.query.filter_by(show_id=show.id).order_by(Episode.episode_number).all()
    maxWatchedEpisode = None

    if current_user.is_authenticated:
      watchedRows = (
        Watched.query
        .filter_by(user_id=current_user.id)
        .all()
      )

      episode_numbers = []

      for w in watchedRows:
        episode = Episode.query.get(w.episode_id)
        if episode and episode.show_id == show.id:
          episode_numbers.append(episode.episode_number)

      if episode_numbers:
        maxWatchedEpisode = max(episode_numbers)

    reviews = (
      Review.query
      .join(User, Review.user_id == User.id)
      .filter(Review.show_id == show.id)
      .add_columns(User.username, Review.rating, Review.review_text)
      .all()
    )

    userReview = (
      Review.query
      .filter_by(user_id=current_user.id, show_id=show.id)
      .first()
    )

    return render_template(
      "show.html",
      show=show,
      episodes=episodes,
      reviews=reviews,
      maxWatchedEpisode=maxWatchedEpisode,
      userReview=userReview
    )


  @app.route("/api/debug/db")
  def debug_db():
    shows = Show.query.all()
    episodes = Episode.query.all()
    users = User.query.all()
    watched = Watched.query.all()
    reviews = Review.query.all()

    return jsonify({
      "shows": [
        {
          "id": s.id,
          "title": s.title,
          "release_year": s.release_year,
          "rating": s.rating,
          "seasons": s.seasons,
          "genres": s.genres
        } for s in shows
      ],
      "episodes": [
        {
          "id": e.id,
          "show_id": e.show_id,
          "episode_number": e.episode_number
        } for e in episodes
      ],
      "users": [
        {
          "id": u.id,
          "username": u.username
        } for u in users
      ],
      "watched": [
        {
          "user_id": w.user_id,
          "episode_id": w.episode_id
        } for w in watched
      ],
      "reviews": [
        {
          "user_id": r.user_id,
          "show_id": r.show_id,
          "rating": r.rating,
          "review_text": r.review_text
        } for r in reviews
      ]
    })

  @app.route("/account")
  @login_required
  def account():
    watch_log = (
      Watched.query
      .join(Episode, Watched.episode_id == Episode.id)
      .join(Show, Episode.show_id == Show.id)
      .filter(Watched.user_id == current_user.id)
      .add_columns(
        Show.title.label("show_title"),
        Show.cover.label("cover"),
        Show.id.label("show_id"),
        Episode.episode_number
      )
      .all()
    )

    reviews = (
      Review.query
      .join(Show, Review.show_id == Show.id)
      .filter(Review.user_id == current_user.id)
      .add_columns(
        Show.title.label("show_title"),
        Review.rating,
        Review.review_text
      )
      .all()
    )

    return render_template(
      "account.html",
      watch_log=watch_log,
      reviews=reviews
    )

  with app.app_context():
    db.create_all()

  @app.route("/watch", methods=["POST"])
  @login_required
  def mark_episode_watched():
    data = request.get_json()
    episode_id = data.get("episode_id")

    episode = Episode.query.get(episode_id)
    if not episode:
      return "", 400

    watched = (
      Watched.query
      .join(Episode, Watched.episode_id == Episode.id)
      .filter(
        Watched.user_id == current_user.id,
        Episode.show_id == episode.show_id
      )
      .first()
    )

    if watched:
      watched.episode_id = episode_id
    else:
      watched = Watched(
        user_id=current_user.id,
        episode_id=episode_id
      )
      db.session.add(watched)

    db.session.commit()
    return "", 204
  
  @app.route("/add-review", methods=["POST"])
  @login_required
  def add_review():
    data = request.get_json()
    show_id = data.get("show_id")
    rating = data.get("rating")
    text = data.get("text")

    review = Review(
      user_id=current_user.id,
      show_id=show_id,
      rating=rating,
      review_text=text
    )

    db.session.add(review)
    db.session.commit()

    return "", 204
  
  @app.route("/save-review", methods=["POST"])
  @login_required
  def save_review():
    data = request.get_json()

    show_id = data.get("show_id")
    rating = data.get("rating")
    text = data.get("text")
    has_review = data.get("has_review")
    review_id = data.get("review_id")

    if has_review:
      review = Review.query.get(review_id)
      if review and review.user_id == current_user.id:
        review.rating = rating
        review.review_text = text
    else:
      review = Review(
        user_id=current_user.id,
        show_id=show_id,
        rating=rating,
        review_text=text
      )
      db.session.add(review)

    db.session.commit()
    return "", 204

  return app

app = createApp()
if __name__ == "__main__":
  app.run(debug=True, port=5001)