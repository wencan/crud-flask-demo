#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户模型
#
# wencan
# 2019-04-12

import attr
import typing
import sqlalchemy
import sqlalchemy.orm
import random
import string
from datetime import datetime, date, time, timedelta
from flask import Flask

import model
import crud
import service
import cmd.rest

sql_types = {
    int: sqlalchemy.Integer,
    str: sqlalchemy.String,
    float: sqlalchemy.Numeric,
    datetime: sqlalchemy.DateTime,
    date: sqlalchemy.Date,
    time: sqlalchemy.Time,
    timedelta: sqlalchemy.Interval,
    bytes: sqlalchemy.Binary,
    bool: sqlalchemy.Boolean,
    dict: sqlalchemy.JSON,
    list: sqlalchemy.ARRAY,
}

# 将通用模型映射为SQL表
def map_to_table(cls, md: sqlalchemy.MetaData) -> typing.NoReturn:
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
        _type = sql_types[column.type]
        
        # 创建sql列
        c = sqlalchemy.Column(column_name, _type, key=column_key, primary_key=primary_key)
        columns.append(c)

    # 创建表对象
    table = sqlalchemy.Table(cls.__tablename__, md, *columns)
    #  映射
    sqlalchemy.orm.mapper(cls, table)


md = sqlalchemy.MetaData()

map_to_table(model.Account, md)
map_to_table(model.User, md)

engine = sqlalchemy.create_engine("mysql+pymysql://root:abcd1234@127.0.0.1:3306/test", echo=True)
session_maker = sqlalchemy.orm.sessionmaker(bind=engine)

account_crud = crud.AccountCrud(session_maker)
user_crud = crud.UserCrud(session_maker)

account_service = service.AccountService(account_crud)
user_service = service.UserService(user_crud, account_crud)

app = Flask("crud-flask-demo")
cmd.rest.register_apis(app, user_service, account_service)

app.run()