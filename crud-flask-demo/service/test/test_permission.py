#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 权限service单元测试
# wencan
# 2019-04-26

import unittest
import unittest.mock as mock
import typing
from datetime import datetime

from .exception import NoRowsForTest
from ... import model
from .. import permission
from ...cmd.abcs import CmdAbstractException

__all__ = ("TestPermissionService", )

class TestPermissionService(unittest.TestCase):
    _roles: typing.Mapping[int, model.Role] = dict({1: model.Role(id=1, name="", permissions="1:readable;1:writeable"),
                                                    2: model.Role(id=2, name="", permissions="2:readable;2:writeable")})
    _user_roles: typing.Iterable[model.UserRole] = (model.UserRole(id=1, user_id=1, role_id=1), model.UserRole(id=2, user_id=1, role_id=2))
    _basic_authorizations: typing.Mapping[str, model.BasicAuthorization] = dict({"1": model.BasicAuthorization(id=1, user_id=1, username="1", password="1")})

    def setUp(self):
        # mock RoleCrud
        MockedRoleCrud = mock.patch.object(permission, "RoleAbstractCrud").start()
        mockedRoleCrud = MockedRoleCrud.return_value
        def get_role(role_id: int) -> model.Role:
            role = self._roles.get(role_id)
            if role is None:
                raise NoRowsForTest()
            return role
        mockedRoleCrud.get_role.side_effect = get_role

        # mock UserRoleCurd
        MockedUserRoleCurd = mock.patch.object(permission, "UserRoleAbstractCrud").start()
        mockedUserRoleCrud = MockedUserRoleCurd.return_value
        def get_roles_by_user(user_id: int) -> typing.Iterable[int]:
            return [user_role.role_id for user_role in self._user_roles if user_role.user_id==user_id]
        mockedUserRoleCrud.get_roles_by_user.side_effect = get_roles_by_user

        # mock BasicAuthorizationAbstractCrud
        MockBasicAuthorizationCrud = mock.patch.object(permission, "BasicAuthorizationAbstractCrud").start()
        mockBasicAuthorizationCrud = MockBasicAuthorizationCrud.return_value
        def verify_username_password(username: str, password: str) -> int:
            auth = self._basic_authorizations.get(username)
            if auth is not None and auth.username == username and auth.password == password:
                return auth.user_id
            raise NoRowsForTest()
        mockBasicAuthorizationCrud.verify_username_password.side_effect = verify_username_password

        self._service = permission.PermissionService(auth_crud=mockBasicAuthorizationCrud, role_crud=mockedRoleCrud, user_role_crud=mockedUserRoleCrud)

    def tearDown(self):
        mock.patch.stopall()
    
    def test_basic_authorization(self):
        # 成功
        self.assertEqual(self._service.basic_authorization(username="1", password="1"), 1)

        # 错误的用户名
        with self.assertRaises(CmdAbstractException) as cm:
            self._service.basic_authorization(username="-1", password="-1")
        ex: CmdAbstractException = cm.exception
        self.assertEqual(ex.http_status, 401)

        # 错误的密码
        with self.assertRaises(CmdAbstractException) as cm:
            self._service.basic_authorization(username="1", password="-1")
        ex: CmdAbstractException = cm.exception
        self.assertEqual(ex.http_status, 401)
    
    def test_get_user_permissions(self):
        # 成功
        self.assertSequenceEqual(self._service.get_user_permissions(1), ("1:readable", "1:writeable", "2:readable", "2:writeable"))

        # 没找到
        self.assertSequenceEqual(self._service.get_user_permissions(2), ())
        

if __name__ == "__main__":
    unittest.main()