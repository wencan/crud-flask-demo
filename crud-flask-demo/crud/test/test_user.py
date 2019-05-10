#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户crud单元测试
# wencan
# 2019-05-09

import unittest
import unittest.mock as mock
import random
import typing
import string
import contextlib

from sqlalchemy.sql import expression
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql import expression
from sqlalchemy.orm import Session, Query
from sqlalchemy.engine import ResultProxy

from ... import model
from .. import user
from ...service.abcs import NoRowsAbstractException

__all__ = ("TestUserCrud", )

class TestUserCrud(unittest.TestCase):
    '''用户crud单元测试'''

    _inserted: typing.MutableMapping[int, model.User] = dict({1: model.User(id=1, account_id=1, account=model.Account(id=1))})

    def setUp(self):
        # mock expression.insert
        # 忽略表模型，直接返回空Insert对象
        mock.patch("sqlalchemy.sql.expression.insert").start()
        expression.insert.return_value = Insert.__new__(Insert)

        # mock Insert.values
        # 用模型对表替代Inserter对象，方便后面的mock
        mock.patch("sqlalchemy.sql.dml.Insert.values").start()
        def insert_user(**kwargs) -> model.User:
            return model.User(id=random.randint(10, 100), account=None, **kwargs)
        Insert.values.side_effect = insert_user

        # mock Session.execute
        # 改为保存到自有集合
        mock.patch("sqlalchemy.orm.Session.execute").start()
        def execute(obj) -> mock.Mock:
            self._inserted[obj.id] = obj
            ret = mock.create_autospec(spec=ResultProxy, instance=True, inserted_primary_key=obj.id)
            return ret
        Session.execute.side_effect = execute

        # mock Session.query
        # 忽略表模型，直接返回空Query对象
        mock.patch("sqlalchemy.orm.Session.query").start()
        Session.query.return_value = Query.__new__(Query)
        
        # mock Query.filter_by.first
        # 改为向自有集合查询
        mock.patch("sqlalchemy.orm.Query.filter_by").start()
        def filter_by(id: int) -> typing.Union[model.User, None]:
            filter = mock.Mock()
            filter.first.side_effect = lambda: self._inserted.get(id)
            return filter
        Query.filter_by.side_effect = filter_by

        # # mock session
        mockedSessionCtx = mock.create_autospec(spec=typing.ContextManager, instance=True)
        mockedSessionCtx.__enter__.return_value = Session()
        mockedSessionMaker = mock.Mock(return_value=mockedSessionCtx)

        # 创建基于mock对象的用户crud对象
        self._crud = user.UserCrud(mockedSessionMaker)
    
    def tearDown(self):
        mock.patch.stopall()
    
    def test_create_user(self):
        account_id = random.randint(10, 100)
        name = "".join([random.choice(string.ascii_lowercase) for n in range(6)])
        phone = "".join([random.choice(string.digits) for n in range(6)])
        user = self._crud.create_user(account_id=account_id, name=name, phone=phone)
        self.assertEqual(user.account_id, account_id)
        self.assertEqual(user.name, name)
        self.assertEqual(user.phone, phone)
    
    def test_get_user(self):
        user = self._crud.get_user(1)

        with self.assertRaises(NoRowsAbstractException):
            self._crud.get_user(1000)

if __name__ == "__main__":
    unittest.main()