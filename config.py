import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    # TODO: e-mail set up
    MAIL_PASSWORD = 'zaiglvdxovmlnuec'
    MAIL_USERNAME = 'jogofbashan@gmail.com'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_USE_TLS = 1
    MAIL_PORT = 587
    ADMINS = ['jogofbashan@gmail.com']
