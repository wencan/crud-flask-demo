#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import model

class AccountService:
    def __init__(self, account_crud):
        self._account_crud = account_crud
    
    def get_account(self, account_id):
        return self._account_crud.get_account(account_id)