# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from flask import session
from flask_oauth import OAuth
from config import OAUTH_CREDENTIALS

AUTH = {
    'facebook': 1,
    'vk':       2,
    'google':   3,
    'yandex':   4
}

oauth = OAuth()
credentials = OAUTH_CREDENTIALS
twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/',
                           request_token_url='https://api.twitter.com/oauth2/request_token',
                           access_token_url='https://api.twitter.com/oauth2/access_token',
                           authorize_url='https://api.twitter.com/oauth2/authorize',
                           consumer_key='AQHivz7uPxuO1TTe7GlCFWHPB',
                           consumer_secret='CuiZoB2DhU6fDGmx9qibWAjUc2EC3uRkhuV4uqDixjYIE4aKgH'
                           )

vk = oauth.remote_app('vk',
                      base_url='https://api.vk.com/',
                      request_token_url=None,
                      access_token_url='https://oauth.vk.com/access_token',
                      authorize_url='https://oauth.vk.com/authorize',
                      consumer_key=credentials['vk']['key'],
                      consumer_secret=credentials['vk']['secret'],
                      request_token_params={'scope': 'email'}
                      )


@vk.tokengetter
def get_vk_token(token=None):
    return session.get('vk_token')


facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=credentials['facebook']['key'],
                            consumer_secret=credentials['facebook']['secret'],
                            request_token_params={'scope': 'email'}
                            )


@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')
