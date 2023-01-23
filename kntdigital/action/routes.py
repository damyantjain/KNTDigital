from flask import Blueprint, render_template, flash, redirect, url_for
from kntdigital.main.forms import LoginForm, RequestResetForm, ResetPasswordForm
from kntdigital.main import utils
from kntdigital import mysql, db, bcrypt
from kntdigital.models.user import User, Action
from flask_login import current_user, login_user, logout_user, login_required
from kntdigital.action.decorator import requires_action_access

action = Blueprint("action", __name__)


@action.route("/action/<int:action_id>")
@login_required
def init_action(action_id):
    if current_user.access.access_name != "ADMIN":
        ids = [element.id for element in current_user.actions]
        if action_id not in ids:
            flash("Not found", "danger")
            return render_template("main/home.html")
    match action_id:
        case 1:
            return render_template("actions/cash_book.html", title="Cash Book")
        case 2:
            return render_template("actions/asset.html", title="Asset")
        case 3:
            return render_template("actions/grocery.html", title="Grocery")
        case 4:
            return render_template("actions/stationary.html", title="Stationary")
        case 5:
            return render_template("actions/employee.html", title="Employee")
        case _:
            return render_template("main/home.html")
