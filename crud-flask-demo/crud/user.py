#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户crud操作
#
# wencan
# 2019-04-13

import typing

from sqlalchemy.orm import Session
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import UserAbstractCrud
from .exceptions import NoRows
from .utils import scoped_session_maker

__all__ = ("UserCrud")


class UserCrud(UserAbstractCrud):
    def __init__(self, scoped_session_maker: typing.Callable[..., typing.ContextManager[Session]]):
        self._scoped_session_maker = scoped_session_maker
    
    def create_user(self, account_id: int, name: str = "", phone: str = "") -> model.User:
        '''创建并返回新账户'''

        with self._scoped_session_maker() as session:
            # 插入新账户
            inserter = expression.insert(model.User).values(name=name, phone=phone, account_id=account_id)
            res = session.execute(inserter)
            user_id = res.inserted_primary_key

            #查询新插入的对象
            user = session.query(model.User).filter_by(id=user_id).first()
            if user is None:
                raise NoRows()
            return user

    
    def get_user(self, user_id) -> model.User:
        '''获得指定用户，没找到返回None'''

        with self._scoped_session_maker() as session:
            user = session.query(model.User).filter_by(id=user_id).first()
            if user is None:
                raise NoRows()
            return user
