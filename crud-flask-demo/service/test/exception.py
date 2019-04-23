#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 单元测试需要的异常
# wencan
# 2019-04-23

from ..abcs import NoRowsAbstractException

__all__ = ("NoRowsForTest")


class NoRowsForTest(NoRowsAbstractException):
    '''not found'''

    pass