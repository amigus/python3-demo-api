# -*- coding: utf-8 -*-
from logging import getLogger
from marshmallow import post_load
from db.models import ThingyType, Thingy
from ...schemas import ma

logger = getLogger(__name__)


class ThingyTypeSchema(ma.Schema):
    class Meta:
        fields = ("id", "tag", "name", "description", "added")
        model = ThingyType
        strict = True

    added = ma.DateTime(dump_only=True)

    @post_load
    def make(self, data, **kwargs):
        logger.debug(f"creating a new Thingy with {data}")
        return ThingyType(**data)


class ThingyTypeListSchema(ma.Schema):
    class Meta:
        fields = ("id", "tag")
        model = ThingyType
        strict = True


class ThingySchema(ma.Schema):
    class Meta:
        fields = ("id", "important", "added", "notes")
        strict = True
        model = Thingy
