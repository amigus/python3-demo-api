# -*- coding: utf-8 -*-
import datetime
import logging
from flask import current_app, jsonify
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256
from webargs.flaskparser import use_kwargs
from db.models import User
from .schemas import PasswordGrantSchema
from .. import limiter
from . import api

logger = logging.getLogger(__name__)


def _grant(access_token):
    expires_in = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]

    if isinstance(expires_in, datetime.timedelta):
        # By default, JWT_ACCESS_TOKEN_EXPIRES contains a timedelta
        # but flask_jwt_extended allows it to be set to an int so
        # we have to handle both cases.
        expires_in = expires_in.seconds
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
    }


@api.route("/token", methods=["POST"])
@limiter.limit("20/hour")
@use_kwargs(PasswordGrantSchema)
def get_access_token(grant_type, username, password, client_id):
    if grant_type == "password" and client_id == current_app.config["CLIENT_ID"]:
        logger.debug("client_id match; verifying the username and password")

        user = User.query.filter_by(email=username).one_or_none()

        if user:
            logger.debug(f"{user.email} matches user {user}")

            # Email verification and password expiration are ignored when testing
            if (
                (user.email_verified and user.pw_expired is None) or current_app.testing
            ) and pbkdf2_sha256.verify(password, user.pw_hash):
                access_token = create_access_token(user.id)
                if logger.level < logging.INFO:
                    logger.debug(
                        f"password matches hash for user {user}; returning"
                        f" access_token {access_token[0:24]}....{access_token[-7:]}"
                    )
                else:
                    logger.info(f"verified password for user: {user}")
                return _grant(access_token), 200
            else:
                logger.info(f"authentication failure for user {user}")

    message = "invalid grant request"

    logger.debug(
        f"{message}: grant_type: '{grant_type}', client_id"
        f" '{client_id[0:9]}....{client_id[-5:]}'"
    )
    return jsonify(dict(message=message)), 401
