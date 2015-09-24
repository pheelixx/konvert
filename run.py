#!/usr/local/www/flask/bin/python
# coding: utf-8
# import pydevd
# pydevd.settrace('localhost', port=9292, stdoutToServer=True, stderrToServer=True)
from app import app
app.debug = True
app.run(host='192.168.128.4')