#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户逻辑
#
# wencan
# 2018-04-13

import model

__all__ = ("UserService")

class UserService:
    def __init__(self, user_crud, account_crud):
        self._user_crud = user_crud
        self._account_crud = account_crud
    
    def get_user(self, user_id) -> model.User:
        '''获取指定用户，没找到错误待定义'''

        user = self._user_crud.get_user(user_id)
        user.account = self._account_crud.get_account(user.account_id)
        return user
    
    def create_user(self, name: str="", phone: str="") -> model.User:
        '''创建用户，并为新用户创建账户，返回携带账户的用户'''

        # 后面需要补上事务
        account = self._account_crud.create_account()
        user = self._user_crud.create_user(name=name, phone=phone, account_id = account.id)
        user.account = account

        return user