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
        user = self._user_crud.get_user(user_id)
        user.account = self._account_crud.get_account(user.account_id)
        return user