from flask import current_app
from flask import render_template, url_for
from flask_mail import Message

from application.app import mail


def send_email(recipients, token):
    subject = "Please confirm your email"
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    template = render_template("activate.html", confirm_url=confirm_url)
    msg = Message(
        subject=subject,
        recipients=[recipients],
        html=template,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )
    mail.send(msg)
