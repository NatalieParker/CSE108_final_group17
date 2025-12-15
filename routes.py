# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from data_structure import User, db, Review

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and request.method == "GET":
        return redirect(url_for("index"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        remember = bool(request.form.get("remember"))

        if not username or not password:
            flash("Please enter a username and password.", "error")
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user, remember=remember)

                # 🔹 NEW: admins go straight to Flask-Admin dashboard
                if getattr(user, "is_admin", False):
                    return redirect(url_for("admin.index"))

                # students/teachers go to normal dashboard
                return redirect(url_for("index"))

            flash("Invalid username or password.", "error")

    return render_template("login.html")



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip().lower()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Please enter a username and a password.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        elif User.query.filter_by(username=username).first():
            flash("This username is already registered.", "error")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please sign in.", "success")
            return redirect(url_for("auth.login"))

    # <-- always return a template if not redirecting
    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for("auth.login"))
