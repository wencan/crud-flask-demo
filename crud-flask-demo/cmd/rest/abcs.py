#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cmd/rest 抽象基类集合
# wencan
# 2019-04-14

from .views.account import AccountAbstractService
from .views.user import UserAbstractService

__all__ = ("AccountAbstractService", "UserAbstractService")