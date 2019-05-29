import logging
import os

from config import Config
from flask import current_app, Flask, request
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler, SMTPHandler


# initialize packages
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'  # name of the view that handles logins
login.login_message = 'Gotta be logged in first. Oopsie.'
mail = Mail()
migrate = Migrate()


def create_app(config_class=Config):
    flapp = Flask(__name__)
    flapp.config.from_object(config_class)

    # configure packages
    flapp.url_map.strict_slashes = False  # optional trailing slash on all URLs

    # bind packages to the flask application
    db.init_app(flapp)
    login.init_app(flapp)
    mail.init_app(flapp)
    migrate.init_app(flapp, db)

    # initialize blueprints
    # these imports needs to happen below the package configurations above
    from app.errors import bp as errors_bp
    flapp.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    flapp.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    flapp.register_blueprint(main_bp)

    if not flapp.debug and not flapp.testing:
        # email error handling
        if flapp.config['MAIL_SERVER']:
            auth = None

            if flapp.config['MAIL_USERNAME'] or flapp.config['MAIL_PASSWORD']:
                auth = (flapp.config['MAIL_USERNAME'],
                        flapp.config['MAIL_PASSWORD'])

            secure = None

            if flapp.config['MAIL_USE_TLS']:
                secure = ()

            mail_handler = SMTPHandler(
                mailhost=(
                    flapp.config['MAIL_SERVER'],
                    flapp.config['MAIL_PORT']),
                fromaddr='no-reply@' + flapp.config['MAIL_SERVER'],
                toaddrs=flapp.config['ADMINS'],
                subject='ItMe error!',
                credentials=auth,
                secure=secure
            )

            mail_handler.setLevel(logging.ERROR)
            flapp.logger.addHandler(mail_handler)

        # file-based error handling
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler(
            'logs/itme.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)

        flapp.logger.addHandler(file_handler)
        flapp.logger.setLevel(logging.INFO)
        flapp.logger.info('ItMe startup')

    return flapp

# the routes module needs to import the app variable above, so it needs to go
# below that declaration to avoid circular imports
from app import models
