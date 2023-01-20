from flask import Blueprint, render_template, flash, redirect, url_for
from kntdigital.main.forms import LoginForm
from kntdigital import mysql

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template("main/home.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM user WHERE email='{form.email.data}'")
        user = cursor.fetchall()
        print(user)
        flash("Login successful!", "success")
        return redirect(url_for("main.home"))
    return render_template("main/login.html", title="Login", form=form)
