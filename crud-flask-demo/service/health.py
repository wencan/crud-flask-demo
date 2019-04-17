#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 健康检测
# wencan
# 2018-04-17

import abc
import attr

from .. import model
from ..cmd.rest.abcs import HealthAbstractService

__all__ = ("HealthAbstractCrud", "HealthService")

class HealthAbstractCrud(abc.ABC):
    '''数据库的健康检测'''

    @abc.abstractmethod
    def get_health(self) -> model.Health:
        '''返回各个数据库的时间信息'''

class HealthService(HealthAbstractService):
    '''健康检测'''

    def __init__(self, health_crud: HealthAbstractCrud):
        self._health_crud = health_crud

    def get_health(self) -> model.Health:
        '''
        返回健康状态。
        包含本地时间、上游服务健康状况
        '''

        # 数据库健康状态——各个数据库的服务器时间
        # 本地服务器时间自动赋值
        health = self._health_crud.get_health()

        return health
