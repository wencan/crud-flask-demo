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

__all__ = ("HealthAbstractService", "HealthAPI")

class HealthAbstractService(abc.ABC):
    '''健康检测'''

    @abc.abstractmethod
    def get_health(self) -> model.Health:
        '''
        返回健康状态。
        包含本地时间、上游服务健康状况
        '''

class HealthAPI(MethodView):
    def __init__(self, service: HealthAbstractService):
        self._service = service
    
    def get(self):
        health = self._service.get_health()
        return flask.jsonify(attr.asdict(health))