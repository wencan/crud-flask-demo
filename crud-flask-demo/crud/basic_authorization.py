#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户角色crud操作
#
# wencan
# 2019-04-18

import typing

from sqlalchemy.orm import Session
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import BasicAuthorizationAbstractCrud
from .exceptions import NoRows
from .utils import scoped_session_maker

__all__ = ("BasicAuthorizationCrud", )

class BasicAuthorizationCrud(BasicAuthorizationAbstractCrud):
    def __init__(self, scoped_session_maker: typing.Callable[..., typing.ContextManager[Session]]):
        self._scoped_session_maker = scoped_session_maker
    
    def verify_username_password(self, username: str, password: str) -> int:
        '''验证用户名和密码，成功返回用户id，否则抛出NoRows'''

        with self._scoped_session_maker() as session:
            basic_auth = session.query(model.BasicAuthorization).filter(model.BasicAuthorization.username==username, model.BasicAuthorization.password==password).first()
            if basic_auth is None:
                raise NoRows()
            return basic_auth.user_id