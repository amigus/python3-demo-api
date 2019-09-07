import enum
import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    and_,
    func,
    or_,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Enum
from sqlalchemy_utils.types.uuid import UUIDType

db = SQLAlchemy()


class User(db.Model):
    id = Column(UUIDType(), default=uuid.uuid4().bytes, primary_key=True)
    pw_hash = Column(String(256), nullable=False)
    pw_expired = Column(DateTime, nullable=True)
    pw_updated = Column(DateTime, default=datetime.utcnow)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_updated = Column(DateTime(timezone=True), server_default=func.now())
    email_verified = Column(DateTime(timezone=True), nullable=True)
    phone_number = Column(String(255), nullable=True)
    phone_number_updated = Column(DateTime, nullable=True)
    phone_number_verified = Column(Boolean, default=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def from_email(cls, email):
        return cls.query.filter_by(email=email)

    def update_pw_hash(self, pw_hash):
        self.pw_hash = pw_hash
        self.pw_updated = datetime.utcnow()
        self.pw_expired = None
        db.session.commit()

    def verify_email(self):
        self.email_updated = self.email_verified = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}, created='{self.created}')"


class UserProfile(db.Model):
    class Visibility(enum.Enum):
        private = 1
        public = 2

    user_id = Column(UUIDType(), ForeignKey(User.id), primary_key=True)
    given_name = Column(String(256), nullable=True)
    family_name = Column(String(256), nullable=True)
    middle_name = Column(String(256), nullable=True)
    nickname = Column(String(256), nullable=True)
    handle = Column(String(16), unique=True, nullable=False, index=True)
    visibility = Column(Enum(Visibility), default="private")
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship(User, backref=backref("profile", uselist=False))

    @classmethod
    def add(cls, user_profile):
        db.session.add(user_profile)
        db.session.commit()

    @classmethod
    def search(cls, user_id, input):  # TODO: make this more robust
        return cls.query.filter(
            and_(
                or_(
                    cls.given_name.like("%{}%".format(input)),
                    cls.family_name.like("%{}%".format(input)),
                    cls.middle_name.like("%{}%".format(input)),
                    cls.nickname.like("%{}%".format(input)),
                    cls.handle.like("%{}%".format(input)),
                ),
                (cls.visibility == UserProfile.Visibility.public),
            )
        )

    def __repr__(self):
        return (
            f"UserProfile(user_id={self.user_id},"
            f"handle='{self.handle}', created='{self.created}')"
        )


class ThingyType(db.Model):
    __table_args__ = (
        Index("thingy_type_user_id_tag_index", "user_id", "tag"),
        UniqueConstraint("user_id", "tag", name="user_tag_unique"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(UUIDType(), ForeignKey(User.id), primary_key=True)
    tag = Column(String(6), nullable=False)
    name = Column(String(48), nullable=False)
    description = Column(String(256), nullable=True)
    added = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship(User)

    @classmethod
    def all_for(cls, user_id):
        return cls.query.filter_by(user_id=user_id)

    @classmethod
    def add(cls, thingy_point):
        db.session.add(thingy_point)
        db.session.commit()


class Thingy(db.Model):
    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey(ThingyType.id), primary_key=True)
    user_id = Column(UUIDType(), ForeignKey(User.id), primary_key=True)
    added = Column(DateTime, default=datetime.utcnow)
    type = relationship(ThingyType, backref="thingy", uselist=False)
    user = relationship(User)


class ThingyNote(db.Model):
    user_id = Column(UUIDType(), ForeignKey(User.id), primary_key=True)
    thingy_id = Column(Integer, ForeignKey(Thingy.id), primary_key=True)
    value = Column(String(5000), nullable=False)
    added = Column(DateTime(timezone=True), server_default=func.now())
    thingy = relationship(Thingy, backref="note", uselist=False)
    user = relationship(User)
