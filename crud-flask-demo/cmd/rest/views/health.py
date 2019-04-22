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

__all__ = ("HealthAbstractService", "HealthView", "HealthHandlers")

class HealthAbstractService(abc.ABC):
    '''健康检测服务抽象基类'''

    @abc.abstractmethod
    def get_health(self) -> model.Health:
        '''
        返回健康状态。
        包含本地时间、上游服务健康状况
        '''


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