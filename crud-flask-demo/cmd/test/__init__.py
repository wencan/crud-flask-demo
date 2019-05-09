#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入全部测试案例和测试套件

import unittest

from ..rest import test as test_rest

__all__ = ("load_tests", )

modules = (test_rest, )

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in modules:
        tests = loader.loadTestsFromModule(module)
        suite.addTests(tests)
    return suite