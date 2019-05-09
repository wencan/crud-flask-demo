#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试user接口
#
# wencan
# 2019-04-28

import unittest
import unittest.mock as mock
import typing
import copy
import random
import string

import flask
from werkzeug.exceptions import NotFound

from ..user import UserHandlers, UserView
from ..... import model
from ...abc_permission import AbstractGuard
from ....abcs import UserAbstractService, CmdAbstractException

__all__ = ("TestUserAPI")

class TestUserAPI(unittest.TestCase):
    # 测试用数据
    _users: typing.MutableMapping[int, model.User] = dict({1: model.User(id=1, account_id=1, account=model.Account(id=1))})

    def setUp(self):
        # mock AbstractGuard
        mockedGuard = mock.create_autospec(AbstractGuard, instance=True)
        mockedGuard.authorization_required.side_effect = lambda fn: fn

        # mock UserAbstractService
        mockedUserService = mock.create_autospec(UserAbstractService, instance=True)
        def get_user(user_id: int) -> model.User:
            user = self._users.get(user_id)
            if user is None:
                raise NotFound()
            return copy.copy(user)
        mockedUserService.get_user.side_effect = get_user
        def create_user(name: str="", phone: str="") -> model.User:
            account = model.Account(id=random.randint(100, 10000))
            user = model.User(id=random.randint(100, 10000), account_id=account.id, account=account, name=name, phone=phone)
            self._users[user.id]=user
            return copy.copy(user)
        mockedUserService.create_user.side_effect = create_user

        # 基于mock对象创建测试对象
        handlers = UserHandlers(mockedGuard, mockedUserService)
        view = UserView.as_view("user_api", handlers)
        app = flask.Flask("Test")
        app.add_url_rule("/users/<int:user_id>", view_func=view, methods=("GET",))
        app.add_url_rule("/users", view_func=view, methods=("POST",))

        # 测试用客户端对象
        self._client = app.test_client()

    def test_get_user(self):
        resp = self._client.get("/users/1")
        self.assertEqual(resp.status_code, 200)

        resp = self._client.get("/users/100000")
        self.assertEqual(resp.status_code, 404)

    def test_create_user(self):
        name = ''.join([random.choice(string.ascii_lowercase) for n in range(6)])
        phone = ''.join([random.choice(string.ascii_lowercase) for n in range(6)])
        resp = self._client.post("/users", data={"name": name, "phone": phone})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["name"], name)
        self.assertEqual(resp.json["phone"], phone)