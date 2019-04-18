#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 异常抽象基类

import abc

__all__ = ("CmdAbstractException", )

class CmdAbstractException(Exception, abc.ABC):
    @property
    @abc.abstractmethod
    def http_status(self):
        '''HTTP状态码'''