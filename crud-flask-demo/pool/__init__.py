#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 连接管理
# 目前只含mysql连接管理
# wencan
# 2019-04-15

from .mydb import MyDB, map_models_to_tables

__all__ = ("MyDB", "map_models_to_tables")