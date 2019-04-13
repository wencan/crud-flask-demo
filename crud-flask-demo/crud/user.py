#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户crud操作
#
# wencan
# 2019-04-13

from sqlalchemy.orm import sessionmaker as SessionMaker
import model

__all__ = ("UserCrud")


class UserCrud:
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker
    
    def get_account(self, account_id) -> model.User:
        session = self._session_maker()
        try:
            user = session.query(model.User).filter(model.User.id==account_id).first()
            return user
        finally:
            session.close()