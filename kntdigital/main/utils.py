from kntdigital import mail
from flask_mail import Message
from flask import url_for


def send_reset_email(user):
    token = user.generate_confirmation_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f"""To reset your password, vist the following link:
{url_for('main.reset_token', token=token, _external = True)}

If you did not make this request then simply ignore and no changes will be made
"""
    mail.send(msg)
