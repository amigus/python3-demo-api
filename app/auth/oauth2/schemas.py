# -*- coding: utf-8 -*-
from ...schemas import ma


class PasswordGrantSchema(ma.Schema):
    grant_type = ma.Constant("password")
    username = ma.Email(required=True)
    password = ma.Str(load_only=True, required=True)
    client_id = ma.Str(required=True)
