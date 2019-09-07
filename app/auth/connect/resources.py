# -*- coding: utf-8 -*-
import logging
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from webargs.flaskparser import use_args, use_kwargs
from db.models import User, UserProfile
from ...schemas import SearchableListQuerySchema
from .schemas import UserProfileSchema, UserProfileListSchema, UserInfoSchema
from .. import limiter
from . import api

logger = logging.getLogger(__name__)


@api.route("/userinfo")
@limiter.limit("3/15seconds")
@jwt_required
def get_userinfo():
    return UserInfoSchema().jsonify(User.query.get_or_404(get_jwt_identity()))


@api.route("/users", methods=["GET"])
@jwt_required
@use_kwargs(SearchableListQuerySchema())
def get_users(search=None, detailed=False, page=None, per_page=None):
    if search:
        users = UserProfile.search(get_jwt_identity(), search)
    else:
        users = UserProfile.query
    users = users.paginate(page, per_page, False).items

    if detailed:
        return UserProfileSchema(many=True).jsonify(users)
    return UserProfileListSchema(many=True).jsonify(users)


@api.route("/users/<uuid:id>")
@jwt_required
def get_user(id):
    return UserProfileSchema().jsonify(UserProfile.query.get_or_404(id))


@api.route("/users/<uuid:user_id>", methods=["PUT"])
@use_args(UserProfileSchema())
def put_user(user_profile, user_id):
    user_profile.user.id = user_id

    logger.debug(f"user_profile is {user_profile} of type {type(user_profile)}")
    try:
        UserProfile.add(user_profile)
    except IntegrityError:
        message = "a user with that email, handle or user_id already exists"

        logger.debug(message, exc_info=True)
        return jsonify(dict(message=message)), 409
    return "", 204
