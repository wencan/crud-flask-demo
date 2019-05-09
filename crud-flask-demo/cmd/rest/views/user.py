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
from werkzeug.exceptions import BadRequest, NotImplemented

from .... import model
from ..abc_permission import AbstractGuard
from ...abcs import UserAbstractService


__all__ = ("UserHandlers", "UserView")


class UserHandlers:
    '''用户接口处理'''

    def __init__(self, guard: AbstractGuard, user_service: UserAbstractService):
        self._user_service = user_service
        self._guard = guard

        # 添加认证检查
        self.get_user = self._guard.authorization_required(self.get_user)
    
    # @guard.authorization_required
    def get_user(self, user_id: int):
        user = self._user_service.get_user(user_id)
        return flask.jsonify(attr.asdict(user))

    def create_user(self):
        name = flask.request.form.get("name", "")
        phone = flask.request.form.get("phone", "")

        user = self._user_service.create_user(name=name, phone=phone)
        return flask.jsonify(attr.asdict(user))


class UserView(MethodView):
    '''用户接口视图'''

    def __init__(self, handlers: UserHandlers):
        self._handlers = handlers

    def get(self, user_id: int):
        '''获取指定用户的信息'''

        return self._handlers.get_user(user_id)

    def post(self):
        '''创建用户'''
        
        return self._handlers.create_user()



