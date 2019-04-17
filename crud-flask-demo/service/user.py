#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户逻辑
#
# wencan
# 2018-04-13

import abc
from ..cmd.rest.abcs import UserAbstractService
from .. import model
from .exceptions import NotFound
from .abc_exceptions import NoRowsAbstractException

__all__ = ("UserAbstractCrud", "AccountAbstractCrud", "UserService")


class UserAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def create_user(self, account_id: int, name: str = "", phone: str = ""):
        '''创建并返回新账户'''

    @abc.abstractmethod
    def get_user(self, account_id) -> model.User:
        '''获得指定用户，没找到返回None'''

class AccountAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def create_account(self, balance: float=0, score: float=0) ->model.Account:
        '''创建并返回新账户'''

    @abc.abstractmethod
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到返回None'''

class UserService(UserAbstractService):
    def __init__(self, user_crud: UserAbstractCrud, account_crud: AccountAbstractCrud):
        self._user_crud = user_crud
        self._account_crud = account_crud
    
    def get_user(self, user_id) -> model.User:
        '''获取指定用户，没找到错误待定义'''

        try:
            user = self._user_crud.get_user(user_id)
        except NoRowsAbstractException:
            raise NotFound("not fount user: {}".format(user_id))
        try:
            user.account = self._account_crud.get_account(user.account_id)
        except NoRowsAbstractException:
            raise NotFound("not found account: {}".format(user_account_id))

        return user
    
    def create_user(self, name: str="", phone: str="") -> model.User:
        '''创建用户，并为新用户创建账户，返回携带账户的用户'''

        # 后面需要补上事务
        account = self._account_crud.create_account()
        user = self._user_crud.create_user(name=name, phone=phone, account_id = account.id)
        user.account = account

        return user
