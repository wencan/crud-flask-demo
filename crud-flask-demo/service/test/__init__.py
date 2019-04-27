#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# service单元测试
# wencan
# 2019-04-16

import unittest

from .test_account import TestAccountService
from .test_user import TestUserService
from .test_health import TestHealthService

__all__ = ("load_tests")

test_cases = (TestAccountService, TestUserService, TestHealthService)

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite