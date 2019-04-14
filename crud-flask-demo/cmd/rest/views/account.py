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

__all__ = ("AccountAPI")


class AccountAPI(MethodView):
    def __init__(self, service):
        self._service = service

    def get(self, user_id: int, account_id: int):
        assert(account_id is not None)

        account = self._service.get_account(account_id)
        return flask.jsonify(attr.asdict(account))

    def post(self, user_id: int, account_id: int):
        '''充值'''

        assert(user_id)
        assert(account_id)

        value = flask.request.form.get("value")
        if value is None:
            raise BadRequest("not value")

        account = self._service.recharge(account_id, value=value)
        return flask.jsonify(attr.asdict(account))