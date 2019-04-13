#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户接口处理
#
# wencan
# 2019-04-13

import attr
import flask
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

__all__ = ("UserAPI")


class UserAPI(MethodView):
    def __init__(self, service):
        self._service = service

    def get(self, user_id: int):
        assert(user_id is not None)

        user = self._service.get_user(user_id)
        return flask.jsonify(attr.asdict(user))
