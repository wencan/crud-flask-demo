#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .health import Health
from .user import User
from .account import Account
from .role import Role
from .user_role import UserRole
from .basic_authorization import BasicAuthorization

__all__ = ("Health", "User", "Account", "Role", "UserRole", "BasicAuthorization", "all_table_models")

all_table_models = (User, Account, Role, UserRole, BasicAuthorization)