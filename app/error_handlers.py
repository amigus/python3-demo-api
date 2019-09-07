# -*- coding: utf-8 -*-
import json
from logging import getLogger

from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound


logger = getLogger(__name__)


def handle_processing_error(error):
    if not error.data or error.data is None:
        return "", error.code

    headers = error.data.get("headers", None)
    messages = error.data.get("messages", ["Invalid request."])

    if headers:
        logger.debug(f"this error message has headers {headers}")
        return jsonify({"errors": messages}), error.code, headers
    else:
        return jsonify({"errors": messages}), error.code


def handle_simple_error(error, message):
    response = error.get_response()

    response.content_type = "application/json"
    response.data = json.dumps({"message": message})
    return response, error.code


def handle_database_error(error):
    if isinstance(error, NoResultFound):
        return "", 404
    return jsonify(dict(message=error.args[0])), 422


def handle_limit_error(error):
    return handle_simple_error(error, "Rate limit exceeded.")


def handle_not_found_error(error):
    return handle_simple_error(error, "Resource not found.")


def handle_syntax_error(error):
    return handle_simple_error(error, "Syntax error in request.")


def handle_oauth2_client_error(error):
    message = f"error attempting OAuth2 grant request"

    if error.response is not None:
        message = f"{message}: response was [{error.response.status_code}]"
        if error.response.content is not None:
            message = f"{message}: {error.response.content}"
    return message, 504
