from flask import Blueprint, render_template, flash, redirect, url_for
from kntdigital.main.forms import LoginForm, RequestResetForm, ResetPasswordForm
from kntdigital.main import utils
from kntdigital import mysql, db, bcrypt
from kntdigital.models.user import User, Action
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint("main", __name__)


@main.route("/home")
@login_required
def home():
    # cursor = mysql.connection.cursor()
    # cursor.execute(f"SELECT * FROM user WHERE email='{current_user.email}'")
    # users = cursor.fetchall()
    users = User.query.all()
    user = User.query.filter_by(email=current_user.email).first()
    if user is None:
        return redirect(url_for("main.login"))
    if user.access.access_name == "ADMIN":
        actions = Action.query.all()
    else:
        actions = user.actions
    return render_template("main/home.html", actions=actions)


@main.route("/")
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Login Unsuccesfull. Please check username and password", "danger")
    return render_template("main/login.html", title="Login", form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("Account does not exist with this email!", "warning")
        else:
            utils.send_reset_email(user)
            flash(
                "An email has been sent with instructions to reset your password",
                "info",
            )
            return redirect(url_for("main.login"))
    return render_template("main/reset_request.html", title="Reset Password", form=form)


@main.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request.html"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated! Please log in to continue", "success")
        return redirect(url_for("main.login"))
    return render_template("main/reset_token.html", title="Reset Password", form=form)
