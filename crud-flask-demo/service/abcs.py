#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cmd/rest 抽象基类集合
# wencan
# 2019-04-14

from .account import AccountAbstractCrud as AccountAbstractCrudA
from .user import AccountAbstractCrud as AccountAbstractCrudU
from .user import UserAbstractCrud

__all__ = ("AccountAbstractCrud", "UserAbstractCrud")

class AccountAbstractCrud(AccountAbstractCrudA, AccountAbstractCrudU):
    pass
