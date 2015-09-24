# coding: utf-8
__author__ = 'Stanislav Varnavsky'

# import urllib, httplib
# import json
# from flask.ext.babel import gettext
# from config import MS_TRANSLATOR_CLIENT_ID, MS_TRANSLATOR_CLIENT_SECRET
#
#
# def microsoft_translate(text, source, target):
#     if MS_TRANSLATOR_CLIENT_ID == '' or MS_TRANSLATOR_CLIENT_SECRET == '':
#         return gettext('Error: translation server not configured')
#     try:
#         params = urllib.urlencode({
#             'client_id': MS_TRANSLATOR_CLIENT_ID,
#             'client_secret': MS_TRANSLATOR_CLIENT_SECRET,
#             'scope': 'http://api.microsofttranslator.com',
#             'grant_type': 'client_credentials'
#         })
#         connection = httplib.HTTPSConnection('datamarket.accesscontrol.windows.net')
#         connection.request('POST', '/v2/OAuth2-13', params)
#         response = json.loads(connection.getresponse().read())
#         token = response[u'access_token']
#
#         connection = httplib.HTTPConnection('api.microsofttranslator.com')
#         params = {
#             'appId': 'Bearer ' + token,
#             'from': source,
#             'to': target,
#             'text': text.encode('utf-8')
#         }
#         connection.request('GET', '/V2/Ajax.svc/Translate?' + urllib.urlencode(params))
#         response = json.loads('{"response":' + connection.getresponse().read().decode('utf-8-sig') + '}')
#         return response['response']
#     except:
#         return gettext('Error: Unexpected error')
