#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import typing

from .. import model
from .. cmd.abcs import AccountAbstractService
from .exceptions import NotFound
from .abcs import AccountRequiredAccountAbstractCrud as AccountAbstractCrud, NoRowsAbstractException

__all__ = ("AccountService", )


class AccountService(AccountAbstractService):
    def __init__(self, account_crud: AccountAbstractCrud, scoped_session_maker: typing.Callable[..., typing.ContextManager]):
        self._account_crud = account_crud
        self._scoped_session_maker = scoped_session_maker
    
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到错误待定义'''

        try:
            account = self._account_crud.get_account(account_id)
        except NoRowsAbstractException:
            raise NotFound(f"not found account: {account_id}")
        
        return account
    
    def recharge(self, account_id: int, value: float) -> model.Account:
        '''充值，并赠送等额积分，返回账户'''

        try:
            with self._scoped_session_maker(subtransactions_supported=True):
                self._account_crud.add_balance(account_id, value)
                account = self._account_crud.add_score(account_id, value)

            account = self._account_crud.get_account(account_id)
        except NoRowsAbstractException:
            raise NotFound(f"not found account: {account_id}")

        return account
