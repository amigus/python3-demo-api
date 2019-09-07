# -*- coding: utf-8 -*-
from logging import getLogger
from marshmallow import post_load
from passlib.hash import pbkdf2_sha256
from db.models import User, UserProfile
from ...schemas import ma


logger = getLogger(__name__)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "registered")
        model = User
        strict = True

    @post_load
    def make_user(self, data, **kwargs):
        logger.debug(f"creating a new User with {data}")
        data["pw_hash"] = pbkdf2_sha256.hash(data["password"])
        del data["password"]
        return User(**data)

    email = ma.Str(required=True)
    password = ma.Str(load_only=True, required=True)
    phone_number = ma.Str(load_only=True, required=False)
    registered = ma.DateTime(attribute="created", dump_only=True)


class UserInfoSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "email",
            "given_name",
            "family_name",
            "nickname",
            "preferred_username",
            "registered",
            "friends",
        )
        model = User
        strict = True

    given_name = ma.Str(attribute="profile.given_name")
    family_name = ma.Str(attribute="profile.family_name")
    nickname = ma.Str(attribute="profile.nickname")
    preferred_username = ma.Str(attribute="profile.handle")
    registered = ma.DateTime(attribute="created")


class UserProfileSchema(ma.Schema):
    class Meta:
        fields = (
            "user",
            "given_name",
            "family_name",
            "nickname",
            "handle",
            "visibility",
        )
        model = UserProfile
        strict = True

    @post_load
    def make_user_profile(self, data, **kwargs):
        logger.debug(f"creating a new UserProfile with {data}")
        return UserProfile(**data)

    user = ma.Nested(UserSchema)
    handle = ma.Str(required=True)
    visibility = ma.Str(load_only=True)
    registered = ma.DateTime(attribute="created", dump_only=True)


class UserProfileListSchema(ma.Schema):
    class Meta:
        fields = ("handle", "user")
        model = UserProfile
        strict = True

    user = ma.URLFor(".user", id="<user.id>")
