from kntdigital import db
from flask_login import UserMixin
from flask import current_app
import jwt


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(60), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def generate_confirmation_token(self, expiration=1800):
        reset_token = jwt.encode(
            {"user_id": self.id}, current_app.config["SECRET_KEY"], algorithm="HS256"
        )
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.image_file}')"
