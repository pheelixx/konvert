# coding: utf-8
__author__ = 'Stanislav Varnavsky'

from jinja2 import Markup


class MomentJS(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, frmt):
        return Markup('<script>document.write(moment("%s").%s)</script>' % (
            self.timestamp.strftime('%Y-%m-%dT%H:%M:%S Z'), frmt))

    def format(self, frmt):
        return self.render('format("%s")' % frmt)

    def calendar(self):
        return self.render('calendar()')

    def from_now(self):
        return self.render('fromNow()')
