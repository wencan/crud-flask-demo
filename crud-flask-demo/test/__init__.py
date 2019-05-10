#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入全部测试案例和测试套件

import unittest

from ..service import test as test_service
from ..cmd import test as test_cmd
from ..crud import test as test_crud

__all__ = ("load_tests", )

modules = (test_service, test_cmd, test_crud)

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in modules:
        tests = loader.loadTestsFromModule(module)
        suite.addTests(tests)
    return suite