#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户权限检查抽象基类
# wencan
# 2019-04-28

import abc
import typing

__all__ = ("AbstractGuard", )

class AbstractGuard(abc.ABC):
    '''用户权限检查抽象基类'''

    @abc.abstractmethod
    def authorization_required(self, f: typing.Callable) -> typing.Callable:
        '''装饰器。检查用户认证信息，认证失败抛出401'''

    @abc.abstractmethod
    def permission_required(self, permission: str) -> typing.Callable:
        '''检查用户是否拥有指定权限，认证失败抛出401， 没权限抛出403'''