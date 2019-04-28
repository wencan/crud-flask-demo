#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 权限服务
# wencan
# 2019-04-18

import abc
import typing
from itertools import chain

from .. import model
from ..cmd.abcs import PermissionAbstractService
from .abcs import RoleAbstractCrud, UserRoleAbstractCrud, BasicAuthorizationAbstractCrud, NoRowsAbstractException
from .exceptions import Unauthorized

__all__ = ("PermissionService", )


class PermissionService(PermissionAbstractService):
    def __init__(self, auth_crud: BasicAuthorizationAbstractCrud, role_crud: RoleAbstractCrud, user_role_crud: UserRoleAbstractCrud):
        self._auth_crud = auth_crud
        self._role_crud = role_crud
        self._user_role_crud = user_role_crud

    def basic_authorization(self, username: str, password: str) -> int:
        '''验证用户名和密码，有效返回用户id，无效抛出认证异常'''
        try:
            user_id = self._auth_crud.verify_username_password(username, password)
            return user_id
        except NoRowsAbstractException:
            raise Unauthorized()

    def get_user_permissions(self, user_id: int) -> typing.Sequence[str]:
        '''查询用户所有权限作用域'''
        role_ids = self._user_role_crud.get_roles_by_user(user_id)
        roles = [self._role_crud.get_role(role_id) for role_id in role_ids]
        permissions = list(chain(*[role.permissions.split(";") for role in roles]))
        return permissions