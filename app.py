from flask import Flask, render_template, jsonify
from data_structure import db, login_manager, Show, Episode, User, Watched, Review
from routes import auth_bp

def createApp() :
  app = Flask(__name__)
  app.config.update(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="sqlite:///cse108webtv.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
  )

  db.init_app(app)
  login_manager.init_app(app)
  app.register_blueprint(auth_bp)

  @app.route("/")
  def home():
    return render_template("login.html")

  @app.route("/index")
  def index():
    shows = Show.query.order_by(Show.title).all()
    return render_template("index.html", shows=shows)
  
  @app.route("/show-db")
  def show_db():
    return render_template("showDB.html")
  
  @app.route("/show/<int:show_id>")
  def show_detail(show_id):
    show = Show.query.get_or_404(show_id)

    episodes = Episode.query.filter_by(show_id=show.id).order_by(Episode.episode_number).all()

    reviews = (
      Review.query
      .join(User, Review.user_id == User.id)
      .filter(Review.show_id == show.id)
      .add_columns(User.username, Review.rating, Review.review_text)
      .all()
    )

    return render_template(
      "show.html",
      show=show,
      episodes=episodes,
      reviews=reviews
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

  with app.app_context():
    db.create_all()

  return app

app = createApp()
if __name__ == "__main__":
  app.run(debug=True, port=5001)