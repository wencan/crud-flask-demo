#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户模型
#
# wencan
# 2019-04-12

import sqlalchemy
from flask import Flask

from . import model
from . import pool
from . import crud
from . import service
from .cmd import rest as cmd_rest


def main():
    pool.map_models_to_tables(model.all)
    mydb = pool.MyDB("mysql+pymysql://root:abcd1234@127.0.0.1:3306/test", echo=True)
    session_maker = mydb.session_maker()

    account_crud = crud.AccountCrud(session_maker)
    user_crud = crud.UserCrud(session_maker)

    account_service = service.AccountService(account_crud)
    user_service = service.UserService(user_crud, account_crud)

    app = Flask("crud-flask-demo")
    cmd_rest.register_apis(app, user_service, account_service)

    app.run()