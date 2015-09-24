# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from config import ADMINS
from decorators import async
from flask import render_template
from flask.ext.mail import Message
from app import app, mail


@async
def send_email_async(message):
    with app.app_context():
        mail.send(message)


def send_email(subject, sender, recipients, text_body, html_body):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.html = html_body
    send_email_async(message)


def follower_notification(followed, follower):
    send_email('[percepht] %s is now following you' % follower.nickname,
               ADMINS[0],
               ['percepht.service@ya.ru'],
               render_template('followed_email.txt', user=followed, follower=follower),
               render_template('followed_email.html', user=followed, follower=follower))
