from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash


def requires_action_access(action_id):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user.access.access_name == "ADMIN":
                return func(*args, **kwargs)
            ids = [element.id for element in current_user.actions]
            if action_id not in ids:
                return redirect(url_for("main.home"))
            return func(*args, **kwargs)

        return decorated_function

    return decorator
