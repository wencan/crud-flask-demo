#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户service单元测试
# wencan
# 2019-04-16

import unittest
import unittest.mock as mock
import copy
from datetime import datetime

from ... import model
from .. import account

__all__ = ("TestAccountService")


class TestAccountService(unittest.TestCase):
    #  测试用数据
    _account1 = model.Account(id=1, balance=0, score=0, created_at=datetime.now(), updated_at=datetime.now())

    def setUp(self):
        # 开始mock
        self._patcher = mock.patch.object(account, "AccountAbstractCrud")
        # mock类
        mockedClass = self._patcher.start()
        # mock实例
        mockedCrud = mockedClass.return_value

        # mock get_account 方法
        def get_account(account_id: int):
            if account_id is 1:
                return copy.copy(self._account1)
            elif account_id is 0:
                return None
            else:
                raise RuntimeError("I am a exception")
        mockedCrud.get_account.side_effect = get_account

        #mock add_balance 方法
        def add_balance(account_id: int, value: float):
            if account_id is 1:
                self._account1.balance += value
                return copy.copy(self._account1)
        mockedCrud.add_balance.side_effect = add_balance

        # mock add_score 方法
        def add_score(account_id: int, value: float):
            if account_id is 1:
                self._account1.score += value
                return copy.copy(self._account1)
        mockedCrud.add_score.side_effect = add_score

        # 基于mock对象创建测试对象
        self._service = account.AccountService(account_crud=mockedCrud)

    def tearDown(self):
        # mock结束
        self._patcher.stop()

    def test_create_account(self):
        self.assertIsNotNone(self._service.get_account(1))

        with self.assertRaises(RuntimeError) as cm:
            self._service.get_account(-1)
        the_exception = cm.exception
        self.assertEqual(the_exception.args, ("I am a exception",))
    
    def test_recharge(self):
        # 先获取旧账户，充值，查看余额和积分（赠送等额积分）
        old_account = self._service.get_account(account_id=1)
        new_account = self._service.recharge(account_id=1, value=100.34)
        self.assertEqual(old_account.balance+100.34, new_account.balance)
        self.assertEqual(old_account.score+100.34, new_account.score)
        


if __name__ == "__main__":
    unittest.main()