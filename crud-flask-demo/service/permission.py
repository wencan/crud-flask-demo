#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 权限服务
# wencan
# 2019-04-18

import abc
import typing
from itertools import chain

from .. import model
from ..cmd.abc_permission import PermissionAbstractService
from .abc_exceptions import NoRowsAbstractException

__all__ = ("BasicAuthorizationAbstractCrud", "RoleAbstractCrud", "UserRoleAbstractCrud", "PermissionService")


class BasicAuthorizationAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def verify_username_password(self, username: str, password: str) -> int:
        '''验证用户名和密码，成功返回用户id，否则抛出NoRows'''

class RoleAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def get_role(self, role_id: int) -> model.Role:
        '''获得指定角色信息（含权限信息）'''


class UserRoleAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def get_roles_by_user(self, user_id: int) -> typing.Iterable[int]:
        '''获得关联到指定用户的角色。即使没关联到角色也返回空序列'''


class PermissionService(PermissionAbstractService):
    def __init__(self, auth_crud: BasicAuthorizationAbstractCrud, role_crud: RoleAbstractCrud, user_role_crud: UserRoleAbstractCrud):
        self._auth_crud = auth_crud
        self._role_crud = role_crud
        self._user_role_crud = user_role_crud

    def basic_authorization(self, username: str, password: str) -> typing.Union[int, None]:
        '''验证用户名和密码，有效返回用户id，无效返回None（偷懒）'''
        try:
            user_id = self._auth_crud.verify_username_password(username, password)
            return user_id
        except NoRowsAbstractException:
            return None

    def get_user_permissions(self, user_id: int) -> typing.Iterable[str]:
        '''查询用户所有权限作用域'''
        role_ids = self._user_role_crud.get_roles_by_user(user_id)
        roles = [self._role_crud.get_role(role_id) for role_id in role_ids]
        permissions = list(chain(*[role.permission_list for role in roles]))
        return permissions