# -*- coding: utf-8 -*-
import json
from uuid import uuid4
from db.test_models import TEST_SUBJECTS
from db.models import User
from ...test import get_authorization_header


def test_get_user(test_client):
    id = TEST_SUBJECTS[0]["id"]
    email = TEST_SUBJECTS[0]["email"]
    password = TEST_SUBJECTS[0]["password"]
    response = test_client.get(
        f"/connect/users/{id}",
        headers=get_authorization_header(test_client, email, password),
    )

    assert response.status_code == 200

    data = json.loads(response.data)

    assert data["user"]["email"] == email


def test_put_user(test_client):
    new_subject = {
        "user": {"email": "new_subject@domain.com", "password": "Rand0mPassw0rd."},
        "given_name": "New",
        "family_name": "Subject",
        "nickname": "New Subjecto",
        "handle": "new_subject123",
        "visibility": "public",
    }
    user_id = uuid4()
    response = test_client.put(
        f"/connect/users/{user_id}", data=json.dumps(new_subject)
    )

    assert response.status_code == 204

    user = User.query.get((user_id))

    assert user.email == new_subject["user"]["email"]


def test_user_info(test_client):
    email = TEST_SUBJECTS[0]["email"]
    password = TEST_SUBJECTS[0]["password"]
    given_name = TEST_SUBJECTS[0]["given_name"]

    response = test_client.get(
        "/connect/userinfo",
        headers=get_authorization_header(test_client, email, password),
    )
    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert response_json["given_name"] == given_name
