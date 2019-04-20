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
from ..service.abcs import AccountAbstractCrud
from .exceptions import NoRows
from .utils import scoped_session_maker

__all__ = ("AccountCrud")


class AccountCrud(AccountAbstractCrud):
    def __init__(self, scoped_session_maker: typing.Callable[..., typing.ContextManager[Session]]):
        self._scoped_session_maker = scoped_session_maker

    def create_account(self, balance: float=0, score: float=0) ->model.Account:
        '''创建并返回新账户'''

        with self._scoped_session_maker() as session:
            # 插入新账户
            inserter = expression.insert(model.Account).values(balance=balance, score=score)
            res = session.execute(inserter)
            account_id = res.inserted_primary_key

            #查询新插入的对象
            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            if account is None:
                raise NoRows()
            return account
    
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户'''

        with self._scoped_session_maker() as session:
            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            if account is None:
                raise NoRows()
            return account
    
    def add_balance(self, account_id: int, value: float):
        '''充值'''

        with self._scoped_session_maker() as session:
            rowcount = session.query(model.Account).filter(model.Account.id==account_id).update({model.Account.balance: model.Account.balance+value})
            if rowcount is 0:
                raise NoRows()
    
    def add_score(self, account_id: int, value: float):
        '''加积分，返回账户'''

        with self._scoped_session_maker() as session:
            rowcount = session.query(model.Account).filter(model.Account.id==account_id).update({model.Account.score: model.Account.score+value})
            if rowcount is 0:
                raise NoRows()
