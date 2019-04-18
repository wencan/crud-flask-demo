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
from .. import permission

__all__ = ("UserAbstractService", "create_user_view")


class UserAbstractService(abc.ABC):
    @abc.abstractmethod
    def get_user(self, user_id) -> model.User:
        '''获取指定用户，没找到错误待定义'''
    
    @abc.abstractmethod
    def create_user(self, name: str="", phone: str="") -> model.User:
        '''创建用户，并为新用户创建账户，返回携带账户的用户'''

def create_user_view(permission_service: permission.PermissionAbstractService, user_service: UserAbstractService) -> MethodView:
    '''创建用户api处理视图，包含权限控制'''

    guard = permission.Guard(permission_service)

    class UserHandlers:
        def __init__(self, user_service: UserAbstractService):
            self._user_service = user_service
        
        @guard.authorization_required
        def get_user(self, user_id: int):
            user = self._user_service.get_user(user_id)
            return flask.jsonify(attr.asdict(user))

        @guard.authorization_required
        def create_user(self):
            name = flask.request.form.get("name", "")
            phone = flask.request.form.get("phone", "")

            user = self._user_service.create_user(name=name, phone=phone)
            return flask.jsonify(attr.asdict(user))
    
    class UserAPI(MethodView):
        def __init__(self, handlers: UserHandlers):
            self._handlers = handlers

        def get(self, user_id: int):
            '''获取指定用户的信息'''

            return self._handlers.get_user(user_id)

        def post(self):
            '''创建用户'''
            
            return self._handlers.create_user()
            
    handlers = UserHandlers(user_service)
    view = UserAPI.as_view("user_api", handlers)

    return view



