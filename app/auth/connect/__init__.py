# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint(__name__, __name__, url_prefix="/connect")

from .resources import get_user, get_users, put_user
