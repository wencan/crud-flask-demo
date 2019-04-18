#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Flask app
#
# wencan
# 2019-04-13

import typing
from flask import Flask, Response
from werkzeug import exceptions

from . import views
from . import abcs
from ..abc_exception import CmdAbstractException

__all__ = ("register_apis")


def register_apis(app: Flask, health_service: abcs.HealthAbstractService, user_service: abcs.UserAbstractService, account_service: abcs.AccountAbstractService) -> typing.NoReturn:
    '''
    注册试图，关联url
    '''

    # 服务器错误处理
    app.register_error_handler(Exception, handle_exceptions)

    # 健康检测
    health_view = views.HealthAPI.as_view("health_api", health_service)
    app.add_url_rule("/health", view_func=health_view, methods=("GET",))

    # 用户
    account_view = views.UserAPI.as_view("user_api", user_service)
    # 获得指定用户
    app.add_url_rule("/users/<int:user_id>", view_func=account_view, methods=("GET",))
    # 创建用户
    app.add_url_rule("/users", view_func=account_view, methods=("POST",))

    # 账户
    account_view = views.AccountAPI.as_view("account_api", account_service)
    # 获得指定账户
    app.add_url_rule("/users/<int:user_id>/accounts/<int:account_id>", view_func=account_view, methods=("GET",))
    # 充值
    app.add_url_rule("/users/<int:user_id>/accounts/<int:account_id>/recharge", view_func=account_view, methods=("POST",))


def handle_exceptions(e: Exception):
    '''
    错误处理
    输出json错误，而非HTML
    '''
    status = 500
    message = ""
    description = ""

    if isinstance(e, CmdAbstractException):
        status = e.http_status
        message = str(e)
    elif isinstance(e, exceptions.HTTPException):
        e = exceptions.HTTPException(e)
        status = e.code
        message = e.name
        description = e.description
    elif isinstance(e, LookupError):
        status = 404
        message = str(e)
    else:
        message = str(e)
    
    response = f'''{{"message": "{message}", "description": "{description}"}}'''

    return Response(response, status=status, mimetype="application/json")
