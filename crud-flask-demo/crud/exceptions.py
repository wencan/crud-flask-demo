#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 异常
# 实现了server的抽象异常基类
# wencan
# 2019-04-17

from ..service.abcs import NoRowsAbstractException

__all__ = ("NoRows", )

class NoRows(NoRowsAbstractException):
    '''没有查询到指定行，或者没有行受更新影响'''
    pass