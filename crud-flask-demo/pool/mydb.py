#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# mysql连接
# 附加数据模型到数据库表的映射
#
# wencan
# 2019-04-15


import attr
import typing
import sqlalchemy
import sqlalchemy.orm
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta
from threading import Thread

__all__ = ("MyDB", "map_models_to_tables")


class MyDB:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._connected = False
    
    def _connect(self) -> typing.NoReturn:
        '''
        连接到数据库
        需要时再连接，会影响fork
        '''

        if self._connected:
            return

        self._engine = sqlalchemy.create_engine(*self._args, **self._kwargs)
        self._seesion_maker = sqlalchemy.orm.sessionmaker(bind=self._engine)
        self._connected = True

        def ping():
            self.server_now()
            print("mysql connected!")

        # 来一次ping操作
        thread = Thread(target=ping, daemon=True)
        thread.start()
    
    def server_now(self) -> datetime:
        session = self._seesion_maker()
        try:
            result = session.execute("SELECT NOW()")
            return result.fetchone()
        finally:
            session.close()

    def session_maker(self, *args, **kwargs) -> sqlalchemy.orm.sessionmaker:
        '''返回sessionmake'''

        self._connect()

        return self._seesion_maker

# 标准基础类型到sqlalchemy类型的映射
_sql_types = {
    int: sqlalchemy.Integer,
    str: sqlalchemy.String,
    float: sqlalchemy.Numeric,
    datetime: sqlalchemy.DateTime,
    date: sqlalchemy.Date,
    time: sqlalchemy.Time,
    timedelta: sqlalchemy.Interval,
    bytes: sqlalchemy.Binary,
    bool: sqlalchemy.Boolean,
    # dict: sqlalchemy.JSON,
    # list: sqlalchemy.ARRAY,
}


def map_to_table(cls, md: sqlalchemy.MetaData) -> typing.NoReturn:
    '''将通用模型映射为SQL表'''

    # 生成表字段列表
    columns: sqlalchemy.Column = []
    for column in attr.fields(cls):
        # 列名
        column_name = column.name
        # 列键
        column_key = column.name
        # 主键
        primary_key = False

        # 模型元数据
        sql_md = column.metadata.get("sql")
        if sql_md:
            if sql_md == "-":   # 忽略
                continue

            parts = sql_md.split(";")
            # 第一部分为列键
            if parts[0] != column_name:
                column_name = parts[0]

            for part in parts[1:]:
                if part == "primary_key":
                    primary_key = True
        
        # 列类型
        # 应该跳过自定义字段
        _type = _sql_types[column.type]
        
        # 创建sql列
        c = sqlalchemy.Column(column_name, _type, key=column_key, primary_key=primary_key)
        columns.append(c)

    # 创建表对象
    table = sqlalchemy.Table(cls.__tablename__, md, *columns)
    #  映射
    sqlalchemy.orm.mapper(cls, table)


def map_models_to_tables(models: typing.Iterable[typing.Any]) -> typing.NoReturn:
    '''映射全部数据模型到数据库表'''

    md = sqlalchemy.MetaData()

    for model in models:
        map_to_table(model, md)