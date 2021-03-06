# example: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
bind = '192.168.128.4:443'
workers = 5
timeout = 60
errorlog = '-'
loglevel = 'info'
accesslog = '-'
proc_name = 'gunicorn_konvert'
certfile = '/usr/local/www/ssl.crt'
keyfile = '/usr/local/www/ssl.key'
reload = True
chdir = '/usr/local/www'
tmp_upload_dir = '/usr/local/www/upload/tmp'