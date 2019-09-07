from logging import getLogger
from sqlalchemy.exc import IntegrityError
# -*- coding: utf-8 -*-
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_args, use_kwargs
from db.models import ThingyType
from ...schemas import SearchableListQuerySchema
from .schemas import ThingyTypeListSchema, ThingyTypeSchema
from . import api

logger = getLogger(__name__)


@api.route("/type", methods=["GET"])
@jwt_required
@use_kwargs(SearchableListQuerySchema())
def get_thingy_types(detailed=False, page=None, per_page=None):
    thingy_types = (
        ThingyType.all_for(get_jwt_identity()).paginate(page, per_page, False).items
    )

    if detailed:
        return ThingyTypeSchema(many=True).jsonify(thingy_types)
    return ThingyTypeListSchema(many=True).jsonify(thingy_types)


@api.route("/type/<int:id>", methods=["GET"])
@jwt_required
def get_thingy_type(id):
    return ThingyTypeSchema(exclude=["id"]).jsonify(
        ThingyType.query.get((id, get_jwt_identity()))
    )


@api.route("/type/<int:id>", methods=["PUT"])
@jwt_required
@use_args(ThingyTypeSchema())
def put_thingy_type(thingy_type, id):
    thingy_type.id = id
    thingy_type.user_id = get_jwt_identity()

    logger.debug(f"thingy_type is {thingy_type} of type {type(thingy_type)}")
    try:
        ThingyType.add(thingy_type)
    except IntegrityError as err:  # TODO: handle NULL and nonunique separately
        message = "a thingy_type with that id or tag already exists"
        logger.debug(message, err)
        return message, 409
    return "", 204
