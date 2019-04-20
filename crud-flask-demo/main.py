#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户模型
#
# wencan
# 2019-04-12

import logging

from . import model
from . import pool
from . import crud
from .crud import scoped_session_maker as ScopedSessionMaker
from . import service
from .cmd import rest as cmd_rest


def main():
    logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s")

    pool.map_models_to_tables(model.all_table_models)
    mydb = pool.MyDB("mysql+pymysql://root:abcd1234@127.0.0.1:3306/test", echo=True)
    session_maker = mydb.session_maker()

    scoped_session_maker = ScopedSessionMaker(session_factory=session_maker)
    health_crud = crud.HealthCrud(scoped_session_maker)
    account_crud = crud.AccountCrud(scoped_session_maker)
    user_crud = crud.UserCrud(scoped_session_maker)
    role_crud = crud.RoleCrud(scoped_session_maker)
    user_role_crud = crud.UserRoleCrud(scoped_session_maker)
    basic_authorization_crud = crud.BasicAuthorizationCrud(scoped_session_maker)

    # scoped_session_maker = ScopedSessionMaker(session_factory=session_maker, subtransactions_supported=True)
    health_service = service.HealthService(health_crud)
    account_service = service.AccountService(account_crud, scoped_session_maker= scoped_session_maker)
    user_service = service.UserService(user_crud, account_crud, scoped_session_maker= scoped_session_maker)
    permission_service = service.PermissionService(basic_authorization_crud, role_crud, user_role_crud)

    services = cmd_rest.Services(
        permission_service= permission_service,
        user_service= user_service, 
        account_service= account_service,
        health_service= health_service,
    )
    cmd_rest.run_restful_app("crud-app_demo", services)