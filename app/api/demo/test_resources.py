# -*- coding: utf-8 -*-
import json
from db.models import ThingyType
from db.test_models import TEST_SUBJECTS
from ...test import get_authorization_header


def test_get_thingy_types(test_client):
    email = TEST_SUBJECTS[0]["email"]
    password = TEST_SUBJECTS[0]["password"]
    response = test_client.get(
        "/thingy/type", headers=get_authorization_header(test_client, email, password)
    )

    assert response.status_code == 200

    data = json.loads(response.data)

    assert 3 == len(data)
    assert [t for t in data if t["id"] == 2][0]["tag"] == "deferred"


def test_get_thingy_type_by_id(test_client):
    email = TEST_SUBJECTS[0]["email"]
    password = TEST_SUBJECTS[0]["password"]
    response = test_client.get(
        "/thingy/type/2", headers=get_authorization_header(test_client, email, password)
    )

    assert response.status_code == 200

    data = json.loads(response.data)

    assert data["tag"] == "deferred"


def test_put_thingy_type(test_client):
    email = TEST_SUBJECTS[0]["email"]
    password = TEST_SUBJECTS[0]["password"]
    new_tt = {"tag": "declined", "name": "Declined"}
    response = test_client.put(
        "/thingy/type/4",
        data=json.dumps(new_tt),
        headers=get_authorization_header(test_client, email, password),
    )

    assert response.status_code == 204

    tt = ThingyType.query.get((4, TEST_SUBJECTS[0]["id"]))

    assert tt.tag == new_tt["tag"]
