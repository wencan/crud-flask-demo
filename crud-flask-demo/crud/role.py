#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户角色crud操作
#
# wencan
# 2019-04-18

import typing

from sqlalchemy.orm import sessionmaker as SessionMaker
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import RoleAbstractCrud
from .exceptions import NoRows

__all__ = ("RoleCrud")


class RoleCrud(RoleAbstractCrud):
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker

    def get_role(self, role_id: int) -> model.Role:
        '''获得指定角色信息（含权限信息）''' 

        session = self._session_maker()
        try:
            role = session.query(model.Role).filter(model.Role.id==role_id).first()
            if role is None:
                raise NoRows()
            return role
        finally:
            session.close()
