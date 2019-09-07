# -*- coding: utf-8 -*-
import json
from flask import current_app

"""gets an access_token and creates an Authorization: Bearer ... header from it

Keyword arguments:
test_client -- the werkzeug test_client
username -- the username
password -- take a guess
Return: a dict() containing a single HTTP header
"""


def get_authorization_header(test_client, username, password):
    response = test_client.post(
        "/oauth2/token",
        json={
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": current_app.config["CLIENT_ID"],
        },
    )
    access_token = json.loads(response.data)["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
