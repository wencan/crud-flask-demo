#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Flask app
#
# wencan
# 2019-04-13

from flask import Flask
import typing
from . import views

__all__ = ("register_apis")


def register_apis(app: Flask, user_service, account_service) -> typing.NoReturn:
    '''
    注册试图，关联url
    '''

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