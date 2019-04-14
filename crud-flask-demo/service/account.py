#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import model

class AccountService:
    def __init__(self, account_crud):
        self._account_crud = account_crud
    
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到错误待定义'''
        return self._account_crud.get_account(account_id)
    
    def recharge(self, account_id: int, value: float) -> model.Account:
        '''充值，并赠送等额积分，返回账户'''

        # 后面需要补上事务
        self._account_crud.add_balance(account_id, value)
        account = self._account_crud.add_score(account_id, value)
        return account
