#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 检查各个数据库的健康状态
# 返回各个数据库的服务器时间
# wencan
# 2019-04-17

from sqlalchemy.orm import sessionmaker as SessionMaker
from sqlalchemy.sql import expression

from .. import model
from ..service.abcs import HealthAbstractCrud

__all__ = ("HealthCrud", )

class HealthCrud(HealthAbstractCrud):
    def __init__(self, session_maker: SessionMaker):
        self._session_maker = session_maker
    
    def get_health(self) -> model.Health:
        '''返回各个数据库的时间信息'''

        session = self._session_maker()
        try:
            rows = session.execute("SELECT NOW()")
            row = rows.fetchone()
            mysql_time = row[0]
        finally:
            session.close()

        health = model.Health(mysql_time=mysql_time)
        return health