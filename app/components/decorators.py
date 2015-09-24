# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from threading import Thread


def async(function):
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.start()
    return wrapper
