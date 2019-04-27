#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 自定义异常类实现
# 实现了cmd的抽象异常基类
# wencan
# 2019-04-17

from ..cmd.abcs import CmdAbstractException

__all__ = ("NotFound", )

class NotFound(CmdAbstractException):
    '''没找到'''

    _http_status = 404
    
    @property
    def http_status(self) -> int:
        return self._http_status

class Unauthorized(CmdAbstractException):
    '''无认证，或认证失败'''

    _http_status = 401

    @property
    def http_status(self) -> int:
        return self._http_status