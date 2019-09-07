# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint(__name__, __name__, url_prefix="/account")

from .resources import confirm, get_reset_token, set_password, verify
