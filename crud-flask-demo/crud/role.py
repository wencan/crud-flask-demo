#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户角色crud操作
#
# wencan
# 2019-04-18

import typing

from sqlalchemy.orm import  Session
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import RoleAbstractCrud
from .exceptions import NoRows
from .utils import scoped_session_maker

__all__ = ("RoleCrud")


class RoleCrud(RoleAbstractCrud):
    def __init__(self, scoped_session_maker: typing.Callable[..., typing.ContextManager[Session]]):
        self._scoped_session_maker = scoped_session_maker

    def get_role(self, role_id: int) -> model.Role:
        '''获得指定角色信息（含权限信息）''' 

        with self._scoped_session_maker() as session:
            role = session.query(model.Role).filter(model.Role.id==role_id).first()
            if role is None:
                raise NoRows()
            return role
