#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 健康检测
# wencan
# 2019-04-17

import attr
import abc
import flask
from flask.views import MethodView

from .... import model
from ...abcs import HealthAbstractService

__all__ = ("HealthView", "HealthHandlers")


class HealthHandlers:
    '''健康检测接口处理'''

    def __init__(self, health_service: HealthAbstractService):
        self._service = health_service
    
    def get_health(self):
        health = self._service.get_health()
        return flask.jsonify(attr.asdict(health))


class HealthView(MethodView):
    '''健康检测接口视图'''

    def __init__(self, handlers: HealthHandlers):
        self._handlers = handlers
    
    def get(self):
        return self._handlers.get_health()