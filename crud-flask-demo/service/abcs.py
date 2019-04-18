#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cmd/rest 抽象基类集合
# wencan
# 2019-04-14

from .account import AccountAbstractCrud as AccountAbstractCrudA
from .user import AccountAbstractCrud as AccountAbstractCrudU, UserAbstractCrud
from .health import HealthAbstractCrud
from .permission import BasicAuthorizationAbstractCrud, RoleAbstractCrud, UserRoleAbstractCrud
from .abc_exceptions import NoRowsAbstractException

__all__ = ("AccountAbstractCrud", 
            "UserAbstractCrud", 
            "BasicAuthorizationAbstractCrud", 
            "RoleAbstractCrud", 
            "UserRoleAbstractCrud",
            "HealthAbstractCrud", 
            "NoRowsAbstractException")

class AccountAbstractCrud(AccountAbstractCrudA, AccountAbstractCrudU):
    pass
 