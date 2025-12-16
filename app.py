import os
from flask import Flask, render_template, jsonify, redirect, url_for, flash, request
from flask_login import current_user, login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from data_structure import db, login_manager, Show, Episode, User, Watched, Review, WatchStatus
from routes import auth_bp
from sqlalchemy import func

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
    template_mode="bootstrap2",
    index_view=AdminIndexView(
      template="admin/adminn.html"
    )
  )

  # Expose your models in the admin UI
  admin.add_view(SecureModelView(User, db.session))
  admin.add_view(SecureModelView(Show, db.session))
  admin.add_view(SecureModelView(Episode, db.session))
  admin.add_view(SecureModelView(Watched, db.session))
  admin.add_view(SecureModelView(Review, db.session))

  @app.route("/")
  def home():
    if current_user.is_authenticated:
        shows = Show.query.order_by(Show.title).all()
        return render_template("index.html", shows=shows)
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

    avg_rating = (
      db.session.query(func.avg(Review.rating))
      .filter(Review.show_id == show.id)
      .scalar()
    )

    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(
            user_id=current_user.id,
            show_id=show.id
        ).first()


    rating_counts = (
      db.session.query(Review.rating, func.count())
      .filter(Review.show_id == show.id)
      .group_by(Review.rating)
      .all()
    )

    rating_map = {r: c for r, c in rating_counts}


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

    current_status = "planned"
    if current_user.is_authenticated:
      ws = WatchStatus.query.filter_by(
        user_id=current_user.id,
        show_id=show.id
      ).first()

      if ws and ws.status:
        current_status = ws.status.strip().lower()

    return render_template(
      "show.html",
      show=show,
      episodes=episodes,
      reviews=reviews,
      maxWatchedEpisode=maxWatchedEpisode,
      avg_rating=round(avg_rating, 2) if avg_rating else None,
      rating_map=rating_map,
      userReview=userReview,
      current_status=current_status
    )
  
  @app.route("/show/<int:show_id>/review", methods=["POST"])
  @login_required
  def add_review(show_id):
    show = Show.query.get_or_404(show_id)
  
    rating = request.form.get("rating", type=int)
    review_text = (request.form.get("review_text") or "").strip()
  
    if rating is None or rating < 1 or rating > 5:
      flash("Rating must be between 1 and 5.", "error")
      return redirect(url_for("show_detail", show_id=show.id))
  
    existing = Review.query.filter_by(user_id=current_user.id, show_id=show.id).first()
  
    if existing:
      existing.rating = rating
      existing.review_text = review_text
    else:
      r = Review(
        user_id=current_user.id,
        show_id=show.id,
        rating=rating,
        review_text=review_text
      )
      db.session.add(r)
  
    db.session.commit()
    flash("Review saved!", "success")
    return redirect(url_for("show_detail", show_id=show.id))



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
  
  @app.route("/status/<int:show_id>", methods=["POST"])
  @login_required
  def set_status(show_id):
      status = request.form.get("status")
  
      ws = WatchStatus.query.filter_by(
          user_id=current_user.id,
          show_id=show_id
      ).first()
  
      if ws:
          ws.status = status
      else:
          ws = WatchStatus(
              user_id=current_user.id,
              show_id=show_id,
              status=status
          )
          db.session.add(ws)
  
      db.session.commit()
      flash("Status updated.", "success")
      return redirect(url_for("show_detail", show_id=show_id))
  @app.route("/user/<username>")
  def user_profile(username):
      user = User.query.filter_by(username=username).first_or_404()
  
      reviews = (
        Review.query
        .join(Show)
        .filter(Review.user_id == user.id)
        .add_columns(Show.title, Review.rating)
        .all()
      )
  
      return render_template("profile.html", user=user, reviews=reviews)
  @app.route("/lists")
  @login_required
  def lists():
      lists = List.query.filter_by(user_id=current_user.id).all()
      return render_template("lists.html", lists=lists)

  return app

app = createApp()
if __name__ == "__main__":
  app.run(debug=True, port=5001)

