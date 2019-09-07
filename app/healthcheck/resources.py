# -*- coding: utf-8 -*-
from . import api, limiter


@api.route("/ok")
@limiter.limit("1/5second")
def ok():
    # TODO: perform a more meaningful healthcheck and return a useful result.
    return "", 204
