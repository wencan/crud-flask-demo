#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户角色权限crud操作
#
# wencan
# 2019-04-18

import typing

from sqlalchemy.orm import sessionmaker as SessionMaker
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import UserRoleAbstractCrud
from .exceptions import NoRows

__all__ = ("UserRoleCrud")


class UserRoleCrud(UserRoleAbstractCrud):
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker

    def get_roles_by_user(self, user_id: int) -> typing.Iterable[int]:
        '''获得关联到指定用户的角色。即使没关联到角色也返回空序列'''

        session = self._session_maker()
        try:
            user_roles = session.query(model.UserRole).filter(model.UserRole.user_id==user_id).all()
            role_ids = [user_role.role_id for user_role in user_roles]
            return role_ids
        finally:
            session.close()