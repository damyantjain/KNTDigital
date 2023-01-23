from flask import Blueprint, render_template, flash, redirect, url_for
from kntdigital.models.user import User, Action
from flask_login import current_user, login_required
from kntdigital.action.decorator import requires_action_access

employee = Blueprint("employee", __name__)

action_id = 5


@employee.route("/action/employee/add")
@login_required
@requires_action_access(action_id=action_id)
def add_employee():
    return render_template("actions/add_employee.html", title="Add employee")
