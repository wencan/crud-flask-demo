#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户crud操作
#
# wencan
# 2019-04-13

from sqlalchemy.orm import sessionmaker as SessionMaker
from sqlalchemy.sql import expression

import model
from service.abcs import UserAbstractCrud

__all__ = ("UserCrud")


class UserCrud(UserAbstractCrud):
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker
    
    def create_user(self, account_id: int, name: str = "", phone: str = ""):
        '''创建并返回新账户'''

        session = self._session_maker()
        try:
            # 插入新账户
            inserter = expression.insert(model.User).values(name=name, phone=phone, account_id=account_id)
            res = session.execute(inserter)
            session.commit()
            user_id = res.inserted_primary_key

            #查询新插入的对象
            account = session.query(model.User).filter(model.User.id==user_id).first()
            return account
        finally:
            session.close()
    
    def get_user(self, account_id) -> model.User:
        '''获得指定用户，没找到返回None'''

        session = self._session_maker()
        try:
            user = session.query(model.User).filter(model.User.id==account_id).first()
            return user
        finally:
            session.close()
