from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Optional, Regexp, ValidationError
from kntdigital.models.user import User
from flask_login import current_user


class AddorEditEmployeeForm(FlaskForm):
    first_name = StringField("First Name*", validators=[DataRequired()])
    last_name = StringField("Last Name*", validators=[DataRequired()])
    email = StringField("Email*", validators=[DataRequired(), Email()])
    phone_number = StringField(
        "Phone",
        validators=[
            Optional(),
            Regexp(
                r"^\+?1?\d{9,15}$",
                message="Invalid phone number. Up to 15 digits allowed.",
            ),
        ],
    )
    choices = [
        ("Male"),
        ("Female"),
        ("Other"),
    ]
    gender = SelectField("Gender", choices=choices, default="Male")
    submit = SubmitField("Save")

    def validate_email(self, email):
        if email.data == current_user.email:
            return
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError(f"That email is taken. Please choose a different one")
