# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint(__name__, __name__, url_prefix="/oauth2")

from .resources import get_access_token
