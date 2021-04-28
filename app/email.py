from threading import Thread

from flask import render_template
from flask_mail import Message
from api import mail, app


def send_async_email(app, msg):
    """
    An asynchronous email function to allow the email to be sent by a background thread.

    :param app: The application instance of the current_app Flask variable
    :param msg: The Message instance to be sent
    """
    # Flask uses contexts to avoid having to pass arguments across functions.
    # mail.send() uses config values from the application context
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Sends an email using flask-mail with the provided parameters.

    :param subject: The subject line of the email
    :param sender: The account sending the email
    :param recipients: The account(s) to receive the email
    :param text_body: The text to be contained in the email
    :param html_body: The html code to be inserted in the email
    """

    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


# Flask-mail supports Cc and Bcc lists

def send_password_reset_email(user):
    """
    Creates the token and payload for the rest password email

    :param user: The user whose email is going to receive the message
    """
    token = user.get_reset_password_token()
    send_email('[Glass Force Wiki] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token)
               )
