# -*- coding: utf-8 -*-
from flask_marshmallow import Marshmallow

ma = Marshmallow()


class PaginatedSchema(ma.Schema):
    page = ma.Integer(required=False)
    per_page = ma.Integer(required=False)


class ListQuerySchema(PaginatedSchema):
    detailed = ma.Boolean(required=False)


class SearchableListQuerySchema(ListQuerySchema):
    search = ma.Str(required=False)
