from flask import Flask, render_template
from data_structure import db, login_manager
from mockdata import mockData

def createApp() :
  app = Flask(__name__)
  app.config.update(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="sqlite:///cse108webtv.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
  )

  db.init_app(app)
  login_manager.init_app(app)

  @app.route("/")
  def index():
    return render_template("index.html")

  with app.app_context():
    db.create_all()
    mockData()

  return app

if __name__ == "__main__":
  createApp().run(debug=True)