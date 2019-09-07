# -*- coding: utf-8 -*-
import logging
import logging.config
import yaml
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from db.models import db
from oauth2 import OAuth2ClientError
from .api import limiter as api_limiter
from .api.demo import api as thingy_blueprint
from .auth import limiter as auth_limiter
from .auth.account import api as account_blueprint
from .auth.connect import api as connect_blueprint
from .auth.oauth2 import api as oauth2_blueprint
from .healthcheck import api as healthcheck_blueprint, limiter as healthcheck_limiter
from .error_handlers import (
    handle_database_error,
    handle_limit_error,
    handle_processing_error,
    handle_not_found_error,
    handle_oauth2_client_error,
)
from .schemas import ma

migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(f"{__name__}.default_settings")
    app.config.from_envvar(f"{__name__.upper()}_SETTINGS")

    if "LOGGING_YAML" not in app.config and app.testing:
        logging.basicConfig(level=logging.DEBUG)
    else:
        with open(app.config.get("LOGGING_YAML"), "rt") as logging_yaml:
            logging.config.dictConfig(yaml.safe_load(logging_yaml.read()))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    ma.init_app(app)

    app.register_blueprint(account_blueprint)
    app.register_blueprint(connect_blueprint)
    app.register_blueprint(oauth2_blueprint)
    app.register_blueprint(healthcheck_blueprint)
    app.register_blueprint(thingy_blueprint)

    app.register_error_handler(OAuth2ClientError, handle_oauth2_client_error)
    app.register_error_handler(SQLAlchemyError, handle_database_error)
    app.register_error_handler(400, handle_processing_error)
    app.register_error_handler(404, handle_not_found_error)
    app.register_error_handler(422, handle_processing_error)
    app.register_error_handler(429, handle_limit_error)

    api_limiter.init_app(app)
    auth_limiter.init_app(app)
    healthcheck_limiter.init_app(app)

    jwt.init_app(app)
    CORS(app)

    return app
