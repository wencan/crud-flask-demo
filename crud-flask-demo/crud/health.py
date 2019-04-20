#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 检查各个数据库的健康状态
# 返回各个数据库的服务器时间
# wencan
# 2019-04-17

import typing

from sqlalchemy.orm import Session
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import HealthAbstractCrud
from .utils import scoped_session_maker

__all__ = ("HealthCrud", )

class HealthCrud(HealthAbstractCrud):
    def __init__(self, scoped_session_maker: typing.Callable[..., typing.ContextManager[Session]]):
        self._scoped_session_maker = scoped_session_maker
    
    def get_health(self) -> model.Health:
        '''返回各个数据库的时间信息'''

        with self._scoped_session_maker() as session:
            rows = session.execute("SELECT NOW()")
            row = rows.fetchone()
            mysql_time = row[0]

        health = model.Health(mysql_time=mysql_time)
        return health