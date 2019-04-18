#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户接口处理
#
# wencan
# 2019-04-13

import abc

import attr
import flask
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from .... import model

__all__ = ("AccountAbstractService", "AccountAPI")


class AccountAbstractService(abc.ABC):
    @abc.abstractmethod
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到错误待定义'''

    @abc.abstractmethod
    def recharge(self, account_id: int, value: float) -> model.Account:
        '''充值，并赠送等额积分，返回账户'''

class AccountAPI(MethodView):
    def __init__(self, service: AccountAbstractService):
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
