#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户逻辑
#
# wencan
# 2018-04-13

import abc
import typing

from ..cmd.abcs import UserAbstractService
from .. import model
from .exceptions import NotFound
from .abcs import UserAbstractCrud, UserRequiredAccountAbstractCrud as AccountAbstractCrud, NoRowsAbstractException

__all__ = ("UserService", )


class UserService(UserAbstractService):
    def __init__(self, user_crud: UserAbstractCrud, account_crud: AccountAbstractCrud, scoped_session_maker: typing.Callable[..., typing.ContextManager]):
        self._user_crud = user_crud
        self._account_crud = account_crud
        self._scoped_session_maker = scoped_session_maker
    
    def get_user(self, user_id) -> model.User:
        '''获取指定用户，没找到错误待定义'''

        try:
            user = self._user_crud.get_user(user_id)
        except NoRowsAbstractException:
            raise NotFound(f"not fount user: {user_id}")
        try:
            user.account = self._account_crud.get_account(user.account_id)
        except NoRowsAbstractException:
            raise NotFound(f"not found account: {user.account_id}")

        return user
    
    def create_user(self, name: str="", phone: str="") -> model.User:
        '''创建用户，并为新用户创建账户，返回携带账户的用户'''

        with self._scoped_session_maker(subtransactions_supported=True):
            account = self._account_crud.create_account()
            user = self._user_crud.create_user(name=name, phone=phone, account_id = account.id)
            user.account = account

        return user
