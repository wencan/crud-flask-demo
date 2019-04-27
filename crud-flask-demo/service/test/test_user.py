#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户service单元测试
# wencan
# 2019-04-26

import unittest
import unittest.mock as mock
import copy
import random
import typing
import string
from contextlib import contextmanager
from datetime import datetime

from ... import model
from .. import user
from .exception import NoRowsForTest
from ...cmd.abcs import CmdAbstractException

__all__ = ("TestUserService", )


class TestUserService(unittest.TestCase):
    #  测试用数据
    _accounts: typing.MutableMapping[int, model.Account] = dict({1: model.Account(id=1, balance=0, score=0, created_at=datetime.now(), updated_at=datetime.now())})
    _users: typing.MutableMapping[int, model.User] = dict({1: model.User(id=1, name="", phone="", account_id=1, account=_accounts[1], created_at=datetime.now(), updated_at=datetime.now())})

    def setUp(self):
        # # 开始mock
        # self._patcher = mock.patch.object(user, "UserAbstractCrud")
        # # mock类
        # mockedClass = self._patcher.start()

        # mock crudc 类型
        MockedUserCrud = mock.patch.object(user, "UserAbstractCrud").start()
        MockedAccountCrud = mock.patch.object(user, "AccountAbstractCrud").start()
        # mock crud 实例
        mockedUserCrud = MockedUserCrud.return_value
        mockAccountCrud = MockedAccountCrud.return_value

        # mock AccountAbstractCrud.create_account方法
        def create_account(balance: float=0, score: float=0) -> model.Account:
            account = model.Account(
                id=random.randint(100, 10000), 
                balance=balance,
                score=score,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self._accounts[account.id] = account
            return account
        mockAccountCrud.create_account.side_effect = create_account
        # mock AccountAbstractCrud.get_account方法
        def get_account(user_id: int) -> model.Account:
            account = self._accounts.get(user_id)
            if account is None:
                raise NoRowsForTest()
            return account
        mockAccountCrud.get_account.side_effect = get_account
        #mock UserAbstractCrud.create_user 方法
        def create_user(account_id: int, name: str = "", phone: str = "") -> model.User:
            user = model.User.__new__(model.User)
            setattr(user, "id", random.randint(100, 1000))
            setattr(user, "name", name)
            setattr(user,"phone", phone)
            setattr(user, "account_id", account_id)
            setattr(user, "created_at", datetime.now())
            setattr(user, "updated_at", datetime.now())
            self._users[user.id] = user
            return user
        mockedUserCrud.create_user.side_effect = create_user
        # mock UserAbstractCrud.get_user 方法
        def get_user(user_id: int) -> model.User:
            user = self._users.get(user_id)
            if user is None:
                raise NoRowsForTest()
            return user
        mockedUserCrud.get_user.side_effect = get_user

        # mock session maker 工厂
        @contextmanager
        def mockedSessionMaker(subtransactions_supported: bool=False):
            yield None

        # 基于mock对象创建测试对象
        self._service = user.UserService(user_crud=mockedUserCrud, account_crud=mockAccountCrud, scoped_session_maker=mockedSessionMaker)

    def tearDown(self):
        # mock结束
        # self.stop()
        mock.patch.stopall()

    def test_create_user(self):
        # 成功
        name: str = "".join(random.choices(string.ascii_lowercase, k=6))
        phone: str = "".join(random.choices(string.digits, k=10))
        user = self._service.create_user(name=name, phone=phone)
        self.assertIsInstance(user, model.User)
        self.assertIsInstance(user.account, model.Account)
        self.assertEqual(name, user.name)
        self.assertEqual(phone, user.phone)

    def test_get_user(self):
        # 成功
        user = self._service.get_user(1)
        self.assertIsInstance(user, model.User)

        # not found
        with self.assertRaises(CmdAbstractException) as cm:
            self._service.get_user(-1)
        ex: CmdAbstractException = cm.exception
        self.assertEqual(ex.http_status, 404)
        

if __name__ == "__main__":
    unittest.main()