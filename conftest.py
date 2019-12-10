import pytest
from passlib.hash import pbkdf2_sha256

# -*- coding: utf-8 -*-
from app import create_app
from db.test_models import TEST_SUBJECTS
from db.models import (
    db,
    User,
    UserProfile,
    ThingyType,
    Thingy,
)


@pytest.fixture()
def app():
    app = create_app()
    context = app.app_context()

    context.push()

    yield app

    context.pop()


@pytest.fixture()
def test_client(database, app):
    testing_client = app.test_client()

    yield testing_client


@pytest.fixture()
def database():
    db.create_all()
    for subject in TEST_SUBJECTS:
        user = User(
            **{
                "id": subject["id"],
                "pw_hash": pbkdf2_sha256.hash(subject["password"]),
                "email": subject["email"],
            }
        )
        profile = UserProfile(
            **{
                "user_id": subject["id"],
                "given_name": subject["given_name"],
                "family_name": subject["family_name"],
                "nickname": subject["given_name"] + "ster",
                "handle": subject["email"].split("@")[0],
                "visibility": subject["visibility"],
            }
        )
        db.session.add(user)
        db.session.add(profile)
        important_tt = ThingyType(
            **{
                "id": 1,
                "user_id": subject["id"],
                "tag": "important",
                "name": "Important",
            }
        )
        db.session.add(important_tt)
        deferred_tt = ThingyType(
            **{"id": 2, "user_id": subject["id"], "tag": "deferred", "name": "Deferred"}
        )
        db.session.add(deferred_tt)
        delayed_tt = ThingyType(
            **{"id": 3, "user_id": subject["id"], "tag": "delayed", "name": "Delayed"}
        )
        db.session.add(delayed_tt)
        thingy = Thingy(
            **{"id": 1, "user_id": subject["id"], "type_id": important_tt.id}
        )
        db.session.add(thingy)

    db.session.commit()

    yield db

    db.drop_all()
