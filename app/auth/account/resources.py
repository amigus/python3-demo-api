# -*- coding: utf-8 -*-
import logging
from urllib.parse import urlencode
from flask import current_app as app, jsonify, request, url_for
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt_claims,
    jwt_required,
)
from sqlalchemy.exc import DatabaseError
from marshmallow.validate import Length
from webargs.flaskparser import use_args
from passlib.hash import pbkdf2_sha256
from emailer.ses_sender import SESSender
from emailer.reset import Reset
from emailer.verify import Verify
from db.models import User
from ...schemas import ma
from ..oauth2.resources import _grant  # TODO: make this accessible and reusable
from ..connect.schemas import UserSchema
from .. import limiter
from . import api

logger = logging.getLogger(__name__)


@api.route("/confirm", methods=["GET", "POST"])
@jwt_required
@limiter.limit("1/hour")
def confirm():
    claims = get_jwt_claims()
    email = get_jwt_identity()
    user = User.from_email(email).one()

    if "confirm" in claims and claims["confirm"] == user.email:
        logger.debug(f"The JWT has a confirm claim that matches {user.email}")
        try:
            user.verify_email()
        except DatabaseError:
            logger.error(f"updating email_verified for {email}", exc_info=True)
            raise
        else:
            return UserSchema().jsonify(user)

    logger.debug(
        f"The JWT for {user.email} does not include the confirm claim; returning 401"
    )
    return "", 401


@api.route("/password", methods=["POST"])
@jwt_required
@limiter.limit("3/8hours")
@use_args(
    {
        "password": ma.Str(
            locations=("form", "json"),  # Must come from the POST body
            required=True,
            validate=Length(min=15, error="Must be at least 15 characters."),
        )
    }
)
def set_password(args):
    password = args["password"]
    claims = get_jwt_claims()
    user = User.from_email(get_jwt_identity()).one()

    if "password" in claims and claims["password"] == user.email:
        logger.debug(
            f"The JWT has a password claim that matches {user.email};"
            " resetting the password"
        )
        try:
            user.update_pw_hash(pbkdf2_sha256.hash(password))
        except DatabaseError:
            logger.error(f"resetting password for {user}", exc_info=True)
            raise
        else:
            return UserSchema().jsonify(user)
    logger.info(
        f"The JWT for {user} does not include the password claim;" " returning 401"
    )
    return "", 401


@api.route("/reset", methods=["GET", "POST"])
@limiter.limit("3/hour,5/day")
@use_args({"email": ma.Email(required=True)})
def get_reset_token(args):
    email = args["email"]
    subject = app.config.get(
        "ACCOUNT_RESET_EMAIL_SUBJECT", "Python3-Demo-App - Account Reset"
    )

    if User.from_email(email):
        jwt = create_access_token(email, user_claims=dict(password=email))

        Reset(
            SESSender(app.config.get("ACCOUNT_RESET_EMAIL_SENDER")),
            subject,
        )(email, _grant(jwt))
    return jsonify(
        dict(
            message=f"Expect an email with subject '{subject}' at that address."
        )
    )


@api.route("/verify", methods=["GET", "POST"])
@limiter.limit("3/hour,5/day")
@use_args({"email": ma.Email(required=True)})
def verify(args):
    email = args["email"]
    subject = app.config.get(
        "ACCOUNT_CONFIRM_EMAIL_SUBJECT", "Python3-Demo-App - Account Verification"
    )

    if User.from_email(email):
        jwt = create_access_token(email, user_claims=dict(confirm=email))

        Verify(
            SESSender(
                app.config.get("ACCOUNT_CONFIRM_EMAIL_SENDER")
            ),
            subject,
        )(
            email,
            f"{request.url_root.rstrip('/')}{url_for('.confirm')}?"
            f"{urlencode(dict(jwt=jwt))}",
        )
    return jsonify(
        dict(
            message=f"Expect an email with subject '{subject}' at that address."
        )
    )
