#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 检查用户权限
# wencan
# 2019-04-18

import typing
from functools import wraps

from flask import request
from werkzeug import exceptions

from ..abcs import PermissionAbstractService

__all__ = ("Guard", )


class Guard:
    '''检查用户是否登录、是否有权限'''

    def __init__(self, service: PermissionAbstractService):
        self._service = service
    
    def authorization_required(self, f: typing.Callable) -> typing.Callable:
        '''检查用户认证信息，认证失败抛出401'''

        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if auth is None:
                raise exceptions.Unauthorized()
            
            # 获取用户id
            user_id = self._service.basic_authorization(auth.username, auth.password)
            if user_id is None:
                raise exceptions.Unauthorized()
            
            return f(*args, **kwargs)
        
        return decorated

    def permission_required(self, permission: str) -> typing.Callable:
        '''检查用户是否拥有指定权限，认证失败抛出401， 没权限抛出403'''

        def wrapper(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                auth = request.authorization
                if auth is None:
                    raise exceptions.Unauthorized()
                
                # 获取用户id
                user_id = self._service.basic_authorization(auth.username, auth.password)
                if user_id is None:
                    raise exceptions.Unauthorized()
                
                # 获取用户所有权限
                permissions = self._service.get_user_permissions(user_id)
                if not permission in permissions:
                    raise exceptions.Forbidden()
                
                return f(*args, **kwargs)
        
            return decorated

        return wrapper