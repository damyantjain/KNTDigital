from flask import Blueprint, render_template, flash, redirect, url_for, request
from kntdigital.models.user import User, Action
from flask_login import current_user, login_required
from kntdigital.action.decorator import requires_action_access
from kntdigital.action.employee.forms import AddorEditEmployeeForm
from kntdigital import db

employee = Blueprint("employee", __name__)

action_id = 5


@employee.route("/action/employee/add", methods=["GET", "POST"])
@login_required
@requires_action_access(action_id=action_id)
def add_employee():
    form = AddorEditEmployeeForm()
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


@employee.route("/action/employee/<int:id>", methods=["GET", "POST"])
@login_required
@requires_action_access(action_id=action_id)
def employee_profile(id):
    is_employee_form_visible = False
    employee = User.query.filter_by(id=id).first()
    image_file = url_for("static", filename=f"profile_pics/{employee.image}")
    employee_form = AddorEditEmployeeForm()
    if employee_form.validate_on_submit():
        employee.first_name = employee_form.first_name.data
        employee.last_name = employee_form.last_name.data
        employee.email = employee_form.email.data
        employee.phone_number = employee_form.phone_number.data
        employee.gender = employee_form.gender.data
        db.session.commit()
        flash("Employee data updated!", "success")
        return redirect(url_for("employee.employee_profile", id=id))
    elif request.method == "POST":
        is_employee_form_visible = True
    elif request.method == "GET":
        employee_form.first_name.data = employee.first_name
        employee_form.last_name.data = employee.last_name
        employee_form.email.data = employee.email
        employee_form.phone_number.data = employee.phone_number
        employee_form.gender.data = employee.gender
        is_employee_form_visible = False
    return render_template(
        "actions/employee_profile.html",
        employee=employee,
        title="Profile",
        employee_form=employee_form,
        image_file=image_file,
        is_employee_form_visible=is_employee_form_visible,
    )
