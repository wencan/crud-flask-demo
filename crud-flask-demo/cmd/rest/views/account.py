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
from .. import permission

__all__ = ("AccountAbstractService", "create_account_view")


class AccountAbstractService(abc.ABC):
    @abc.abstractmethod
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到错误待定义'''

    @abc.abstractmethod
    def recharge(self, account_id: int, value: float) -> model.Account:
        '''充值，并赠送等额积分，返回账户'''

def create_account_view(permission_service: permission.PermissionAbstractService, account_service: AccountAbstractService) -> MethodView:
    '''创建账户api处理视图，包含权限控制'''
    guard = permission.Guard(permission_service)

    class AccountHandlers:
        def __init__(self, account_service: AccountAbstractService):
            self._account_service = account_service
        
        @guard.permission_required("account:readable")
        def get_account(self, account_id: int):
            account = self._account_service.get_account(account_id)
            return flask.jsonify(attr.asdict(account))
        
        @guard.permission_required("account:writable")
        def recharge(self, account_id: int):
            value = flask.request.form.get("value")
            if value is None:
                raise BadRequest("not value")

            account = self._account_service.recharge(account_id, value=value)
            return flask.jsonify(attr.asdict(account))


    class AccountAPI(MethodView):
        def __init__(self, handlers: AccountHandlers):
            self._handlers = handlers

        def get(self, user_id: int, account_id: int):
            return self._handlers.get_account(account_id)

        def post(self, user_id: int, account_id: int):
            '''目前仅支持充值'''

            return self._handlers.recharge(account_id)

    handlers = AccountHandlers(account_service)
    view = AccountAPI.as_view("account_api", handlers)

    return view