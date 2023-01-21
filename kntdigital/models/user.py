from kntdigital import db, login_manager
from flask_login import UserMixin
from flask import current_app
import jwt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_actions = db.Table(
    "user_actions",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("action_id", db.Integer, db.ForeignKey("action.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(60), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    access_id = db.Column(db.Integer, db.ForeignKey("access.id"), nullable=False)
    access = db.relationship("Access", backref="access", lazy=True)
    actions = db.relationship(
        "Action", secondary=user_actions, backref="actions", lazy=True
    )

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
        return f"User('{self.username}', '{self.email}', {self.image_file}', '{self.access}', {self.access_data})"


class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_name = db.Column(db.String(60), nullable=False)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actionName = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Action('{self.id}', '{self.actionName}')"


class User_Actions(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    action_id = db.Column(db.Integer, db.ForeignKey("action.id"), primary_key=True)
