# -*- coding: utf-8 -*-
import json
from db.test_models import TEST_SUBJECTS
from flask import current_app as app


def test_token(test_client):
    username = TEST_SUBJECTS[0]["email"]
    password = TEST_SUBJECTS[0]["password"]

    response = test_client.post(
        "/oauth2/token",
        json={
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": app.config["CLIENT_ID"],
        },
    )
    assert response.status_code == 200
    assert json.loads(response.data.decode("utf8"))["access_token"]
