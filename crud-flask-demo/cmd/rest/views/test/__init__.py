#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入接口测试案例
#
# wencan
# 2019-04-28

import unittest

from .test_account import TestAccountAPI
from .test_user import TestUserAPI

__all__ = ("load_tests")

test_cases = (TestAccountAPI, TestUserAPI)

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite
