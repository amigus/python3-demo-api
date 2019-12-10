# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint(__name__, __name__, url_prefix="/thingy")

from .resources import get_thingy_type, get_thingy_types, put_thingy_type
