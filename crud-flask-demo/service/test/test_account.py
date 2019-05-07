#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户service单元测试
# wencan
# 2019-04-16

import unittest
import unittest.mock as mock
import copy
import typing
import random
from datetime import datetime

from ... import model
from .. import account
from .exception import NoRowsForTest
from ...cmd.abcs import CmdAbstractException
from ..abcs import AccountRequiredAccountAbstractCrud as AccountAbstractCrud

__all__ = ("TestAccountService", )


class TestAccountService(unittest.TestCase):
    #  测试用数据
    _accounts: typing.MutableMapping[int, model.Account] = dict({1: model.Account(id=1, balance=0, score=0)})

    def setUp(self):
        # mock AccountAbstractCrud
        mockedCrud = mock.create_autospec(AccountAbstractCrud, instance=True)
        # account_id == 1，成功
        # account_id == 0，无效account_id
        # 否则抛出运行时异常
        def get_account(account_id: int) -> model.Account:
            account = self._accounts.get(account_id)
            if account is None:
                raise NoRowsForTest()
            return copy.copy(account)
        mockedCrud.get_account.side_effect = get_account
        #mock AccountAbstractCrud.add_balance 方法
        def add_balance(account_id: int, value: float) -> model.Account:
            account = self._accounts.get(account_id)
            if account is None:
                raise NoRowsForTest()
            account.balance += value
            return copy.copy(account)
        mockedCrud.add_balance.side_effect = add_balance
        # mock AccountAbstractCrud.add_score 方法
        def add_score(account_id: int, value: float) -> model.Account:
            account = self._accounts.get(account_id)
            if account is None:
                raise NoRowsForTest()
            account.score += value
            return copy.copy(account)
        mockedCrud.add_score.side_effect = add_score

        # mock session maker 工厂
        mockedSessionMaker = mock.Mock(return_value=mock.create_autospec(spec=typing.ContextManager, instance=True))

        # 基于mock对象创建测试对象
        self._service = account.AccountService(account_crud=mockedCrud, scoped_session_maker=mockedSessionMaker)

    def test_get_account(self):
        # 成功
        self.assertIsNotNone(self._service.get_account(1))

        # 无效 account_id
        with self.assertRaises(CmdAbstractException) as cm:
            self._service.get_account(0)
        the_exception: CmdAbstractException = cm.exception
        self.assertEqual(the_exception.http_status, 404)

    
    def test_recharge(self):
        # 先获取旧账户，充值，查看余额和积分（赠送等额积分）

        # 成功
        value = random.uniform(100, 500)
        old_account = self._service.get_account(account_id=1)
        new_account = self._service.recharge(account_id=1, value=value)
        self.assertEqual(old_account.balance+value, new_account.balance)
        self.assertEqual(old_account.score+value, new_account.score)

        self.assertIsNotNone(self._service.get_account(1))

        # 无效 account_id
        with self.assertRaises(CmdAbstractException) as cm:
            new_account = self._service.recharge(account_id=0, value=value)

        # 异常
        with self.assertRaises(Exception) as cm:
            new_account = self._service.recharge(account_id=-1, value=value)
        


if __name__ == "__main__":
    unittest.main()