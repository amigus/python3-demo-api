# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


api = Blueprint(__name__, __name__, url_prefix="/healthcheck")
limiter = Limiter(key_func=get_remote_address)

from .resources import ok
