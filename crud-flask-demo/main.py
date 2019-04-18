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
    pool.map_models_to_tables(model.all_table_models)
    mydb = pool.MyDB("mysql+pymysql://root:abcd1234@127.0.0.1:3306/test", echo=True)
    session_maker = mydb.session_maker()

    health_crud = crud.HealthCrud(session_maker)
    account_crud = crud.AccountCrud(session_maker)
    user_crud = crud.UserCrud(session_maker)
    role_crud = crud.RoleCrud(session_maker)
    user_role_crud = crud.UserRoleCrud(session_maker)
    basic_authorization_crud = crud.BasicAuthorizationCrud(session_maker)

    health_service = service.HealthService(health_crud)
    account_service = service.AccountService(account_crud)
    user_service = service.UserService(user_crud, account_crud)
    permission_service = service.PermissionService(basic_authorization_crud, role_crud, user_role_crud)

    app = Flask("crud-flask-demo")
    services = cmd_rest.Services(
        permission_service= permission_service,
        user_service= user_service, 
        account_service= account_service,
        health_service= health_service,
    )
    cmd_rest.register_apis(app, services)

    app.run()