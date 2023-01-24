from flask import Blueprint, render_template, flash, redirect, url_for
from kntdigital.models.user import User, Action
from flask_login import current_user, login_required
from kntdigital.action.decorator import requires_action_access
from kntdigital.action.employee.forms import AddEmployeeForm
from kntdigital import db

employee = Blueprint("employee", __name__)

action_id = 5


@employee.route("/action/employee/add", methods=["GET", "POST"])
@login_required
@requires_action_access(action_id=action_id)
def add_employee():
    form = AddEmployeeForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            gender=form.gender.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Employee has been successfully added!", "success")
        return redirect(url_for("action.init_action", action_id=action_id))
    return render_template("actions/add_employee.html", title="Add employee", form=form)
