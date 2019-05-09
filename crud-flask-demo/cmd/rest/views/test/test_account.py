#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试account接口
#
# wencan
# 2019-04-28

import unittest
import unittest.mock as mock
import copy
import typing

import flask
from werkzeug.exceptions import NotFound

from ..account import AccountHandlers, AccountView
from ..... import model
from ...abc_permission import AbstractGuard
from ....abcs import AccountAbstractService, CmdAbstractException

__all__ = ("TestAccountAPI")

class TestAccountAPI(unittest.TestCase):
    #  测试用数据
    _accounts: typing.MutableMapping[int, model.Account] = dict({1: model.Account(id=1, balance=0, score=0)})

    def setUp(self):
        # mock AbstractGuard
        mockedGuard = mock.create_autospec(AbstractGuard, instance=True)
        mockedGuard.permission_required.side_effect = lambda s: lambda fn: fn

        # mock AccountAbstractService
        mockedAccountService = mock.create_autospec(AccountAbstractService, instance=True)        
        def get_account(account_id: int) -> model.Account:
            account = self._accounts.get(account_id)
            if account is None:
                raise NotFound()
            return copy.copy(account)
        mockedAccountService.get_account.side_effect = get_account
        def recharge(account_id: int, value: float) -> model.Account:
            account = self._accounts.get(account_id)
            if account is None:
                raise NotFound()
            account.balance += value
            return copy.copy(account)
        mockedAccountService.recharge.side_effect = recharge

        # 基于mock对象创建测试对象
        handlers = AccountHandlers(mockedGuard, mockedAccountService)
        view = AccountView.as_view("account_api", handlers)
        app = flask.Flask("Test")
        app.add_url_rule("/users/<int:user_id>/accounts/<int:account_id>", view_func=view, methods=("GET",))
        app.add_url_rule("/users/<int:user_id>/accounts/<int:account_id>/recharge", view_func=view, methods=("POST",))

        # 测试用客户端对象
        self._client = app.test_client()

    def test_get_account(self):
        resp = self._client.get("/users/1/accounts/1")
        self.assertEqual(resp.status_code, 200)

        resp = self._client.get("/users/1/accounts/100")
        self.assertEqual(resp.status_code, 404)
    
    def test_recharge(self):
        resp = self._client.get("/users/1/accounts/1")
        self.assertEqual(resp.status_code, 200)
        balance = resp.json["balance"]
        resp = self._client.post("/users/1/accounts/1/recharge", data={"value": 100})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(balance+100, resp.json["balance"])

        resp = self._client.post("/users/1/accounts/100/recharge", data={"value": 100})
        self.assertEqual(resp.status_code, 404)
