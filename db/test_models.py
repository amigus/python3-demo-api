from db.models import User, UserProfile

import uuid

TEST_SUBJECTS = [
    {
        "id": uuid.uuid4(),
        "email": "user1@domain.com",
        "password": "passw0rd!",
        "email_verified": True,
        "given_name": "test gn 1",
        "family_name": "test fn 1",
        "visibility": "public",
    },
    {
        "id": uuid.uuid4(),
        "email": "user2@domain.com",
        "password": "passw0rd!",
        "email_verified": True,
        "given_name": "test gn 2",
        "family_name": "test fn 2",
        "visibility": "public",
    },
    {
        "id": uuid.uuid4(),
        "email": "user3@domain.com",
        "password": "passw0rd!",
        "email_verified": True,
        "given_name": "test gn 3",
        "family_name": "test fn 3",
        "visibility": "private",
    },
    {
        "id": uuid.uuid4(),
        "email": "user4@domain.com",
        "password": "passw0rd!",
        "email_verified": False,
        "given_name": "test gn 4",
        "family_name": "test fn 4",
        "visibility": "public",
    },
    {
        "id": uuid.uuid4(),
        "email": "user5@domain.com",
        "password": "passw0rd!",
        "email_verified": False,
        "given_name": "test gn 5",
        "family_name": "test fn 5",
        "visibility": "private",
    },
]


def test_user_query_first(app, database):
    subject = TEST_SUBJECTS[0]
    user = User.query.order_by(User.created).first()

    assert user.email == subject["email"]


def test_user_query_by_id(app, database):
    subject = TEST_SUBJECTS[1]
    user = User.query.get(subject["id"])

    assert user.email == subject["email"]


def test_user_profile_by_id(app, database):
    subject = TEST_SUBJECTS[0]
    user = User.query.get(subject["id"])
    profile = UserProfile.query.get(subject["id"])

    assert profile.given_name == subject["given_name"]
    assert profile.visibility == UserProfile.Visibility.public


def test_user_profile_relationship(app, database):
    subject = TEST_SUBJECTS[0]
    user = User.query.get(subject["id"])

    assert user.profile.given_name == subject["given_name"]


def test_user_profile_search(app, database):
    subject = TEST_SUBJECTS[1]

    assert (
        subject["given_name"] == UserProfile.search(
            subject["id"],
            "gn 2"
        ).first().given_name
    )

    subject = TEST_SUBJECTS[0]

    assert (
        subject["given_name"] == UserProfile.search(
            subject["id"],
            "test gn"
        ).first().given_name
    )
    assert (
        subject["given_name"] == UserProfile.search(
            subject["id"],
            "t gn"
        ).first().given_name
    )
