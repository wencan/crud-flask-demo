#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 权限抽象基类
# wencan
# 2019-04-18

import abc
import typing


__all__ = ("PermissionAbstractService", )


class PermissionAbstractService(abc.ABC):
    @abc.abstractmethod
    def basic_authorization(self, username: str, password: str) -> typing.Union[int, None]:
        '''验证用户名和密码，有效返回用户id，无效返回None'''

    @abc.abstractmethod
    def get_user_permissions(self, user_id: int) -> typing.Iterable[str]:
        '''查询用户所有权限作用域'''
