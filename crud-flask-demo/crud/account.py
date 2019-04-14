#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户crud操作
#
# wencan
# 2019-04-13

from sqlalchemy.orm import sessionmaker as SessionMaker
from sqlalchemy.sql import expression
import model

__all__ = ("AccountCrud")

sql_insert_empty_account = r'''INSERT INTO basic_account'''


class AccountCrud:
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker

    def create_account(self, balance: float=0, score: float=0) ->model.Account:
        '''创建并返回新账户'''

        session = self._session_maker()
        try:
            # 插入新账户
            inserter = expression.insert(model.Account).values(balance=balance, score=score)
            res = session.execute(inserter)
            session.commit()
            account_id = res.inserted_primary_key

            #查询新插入的对象
            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            return account
        finally:
            session.close()
    
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到返回None'''

        session = self._session_maker()
        try:
            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            return account
        finally:
            session.close()
    
    def add_balance(self, account_id: int, value: float) -> model.Account:
        '''充值，返回账户'''

        session = self._session_maker()
        try:
            session.query(model.Account).filter(model.Account.id==account_id).update({model.Account.balance: model.Account.balance+value})
            session.commit()

            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            return account
        finally:
            session.close()
    
    def add_score(self, account_id: int, value: float) -> model.Account:
        '''加积分，返回账户'''

        session = self._session_maker()
        try:
            session.query(model.Account).filter(model.Account.id==account_id).update({model.Account.score: model.Account.score+value})
            session.commit()

            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            return account
        finally:
            session.close()
