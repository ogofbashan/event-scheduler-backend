from flask_mail import Message
from app import app, mail
from flask import render_template

def sendMail(title, day, month, year, notes, email):
    msg = Message(
        subject = 'Event Saved: ' + title,
        sender = app.config['ADMINS'][0],
        recipients = [email]
    )

    # set the text and html body ot a template render
    msg.body = render_template(
        'email/event_saved.txt',
        title=title, day=day, month=month, year=year, notes=notes, email=email
    )

    msg.html = render_template(
        'email/event_saved.html',
        title=title, day=day, month=month, year=year, notes=notes, email=email
    )

    mail.send(msg)
