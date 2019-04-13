#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户crud操作
#
# wencan
# 2019-04-13

from sqlalchemy.orm import sessionmaker as SessionMaker
import model

__all__ = ("AccountCrud")


class AccountCrud:
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker
    
    def get_account(self, account_id) -> model.Account:
        session = self._session_maker()
        try:
            account = session.query(model.Account).filter(model.Account.id==account_id).first()
            return account
        finally:
            session.close()