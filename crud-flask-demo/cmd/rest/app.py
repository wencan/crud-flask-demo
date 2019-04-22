#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Flask app
#
# wencan
# 2019-04-13

import attr
import typing
import logging

from flask import Flask, Response
from flask.logging import default_handler as flask_default_logging_handler
from werkzeug import exceptions

from . import views
from . import abcs
from . import permission
from ..abc_exception import CmdAbstractException

__all__ = ("run_restful_app", "Services")

log = logging.getLogger(__name__)


@attr.attrs(auto_attribs=True)
class Services:
    permission_service: permission.PermissionAbstractService
    user_service: abcs.UserAbstractService
    account_service: abcs.AccountAbstractService
    health_service: abcs.HealthAbstractService


def run_restful_app(name: str, services: Services, host: str=None, port: int=None, debug: bool=False) -> None:
    '''
    创建app，配置，然后运行
    '''
    app = Flask(name)
    app.logger.removeHandler(flask_default_logging_handler)

    # 服务器错误处理
    app.register_error_handler(Exception, handle_exceptions)

    # 健康检测
    health_handlers = views.HealthHandlers(services.health_service)
    health_view = views.HealthView.as_view("health_api", health_handlers)
    app.add_url_rule("/health", view_func=health_view, methods=("GET",))

    # 用户
    user_handlers = views.UserHandlers(services.permission_service, services.user_service)
    user_view = views.UserView.as_view("user_api", user_handlers)
    # 获得指定用户
    app.add_url_rule("/users/<int:user_id>", view_func=user_view, methods=("GET",))
    # 创建用户
    app.add_url_rule("/users", view_func=user_view, methods=("POST",))

    # 账户
    account_handlers = views.AccountHandlers(services.permission_service, services.account_service)
    account_view = views.AccountView.as_view("account_api", account_handlers)
    # 获得指定账户
    app.add_url_rule("/users/<int:user_id>/accounts/<int:account_id>", view_func=account_view, methods=("GET",))
    # 充值
    app.add_url_rule("/users/<int:user_id>/accounts/<int:account_id>/recharge", view_func=account_view, methods=("POST",))

    # run
    app.run(host=host, port=port, debug=debug)


def handle_exceptions(e: Exception):
    '''
    错误处理
    输出json错误，而非HTML
    '''

    status = 500
    message = ""
    description = ""

    if isinstance(e, CmdAbstractException):
        # 自己主动抛出的异常，不再重复输出
        status = e.http_status
        message = str(e)
    elif isinstance(e, exceptions.HTTPException):
        log.exception(e)

        status = e.code
        message = e.name
        description = e.description
    else:
        log.exception(e)

        message = str(e)
    
    response = f'''{{"message": "{message}", "description": "{description}"}}'''

    return Response(response, status=status, mimetype="application/json")
