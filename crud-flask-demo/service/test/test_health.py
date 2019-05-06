#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 健康service单元测试
# wencan
# 2019-04-26

import unittest
import unittest.mock as mock
import typing
from datetime import datetime

from .. import health
from ... import model
from .. import health

__all__ = ("TestHealthService", )


class TestHealthService(unittest.TestCase):
    mysql_errmsg = "dbase broken"

    def setUp(self):
        # mock HealthAbstractService
        MockHealthCrud = mock.patch.object(health, "HealthAbstractService").start()
        mockHealthCrud = MockHealthCrud.return_value
        # mock HealthAbstractService.get_health方法
        def get_health() -> model.Health:
            health = model.Health.__new__(model.Health)
            health.mysql_time = str(datetime.now())
            health.server_time = str(datetime.now())
            return health
        # 第一次调用成功，第二次抛出异常
        mockHealthCrud.get_health.side_effect = mock.MagicMock(side_effect=(get_health(), RuntimeError(self.mysql_errmsg)))

        # 基于mock对象创建测试对象
        self._service = health.HealthService(mockHealthCrud)
    
    def tearDown(self):
        mock.patch.stopall()
    
    def test_get_health(self) -> model.Health:
        # 成功
        h = self._service.get_health()
        self.assertIsInstance(h, model.Health)
        self.assertIsInstance(datetime.strptime(h.mysql_time, "%Y-%m-%d %H:%M:%S.%f"), datetime)

        # 异常
        h = self._service.get_health()
        # 当mysql发生异常时，mysql_time应该是异常消息
        self.assertEqual(h.mysql_time, self.mysql_errmsg)
    

if __name__ == "__main__":
    unittest.main()