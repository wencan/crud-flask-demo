#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cmd接口模块的抽象基类
# 从cmd各个下级模块移出
# 需要service模块实现
# 被cmd下级模块和service模块所依赖
# wencan
# 2019-04-22

import abc
import typing

from .. import model

__all__ = (
            "PermissionAbstractService", 
            "AccountAbstractService",
            "UserAbstractService",
            "HealthAbstractService",
            "CmdAbstractException", 
            )


class CmdAbstractException(Exception, abc.ABC):
    '''cmd异常抽象基类'''

    @property
    @abc.abstractmethod
    def http_status(self) -> int:
        '''HTTP状态码'''


class PermissionAbstractService(abc.ABC):
    @abc.abstractmethod
    def basic_authorization(self, username: str, password: str) -> int:
        '''验证用户名和密码，有效返回用户id，无效抛出认证异常'''

    @abc.abstractmethod
    def get_user_permissions(self, user_id: int) -> typing.Sequence[str]:
        '''查询用户所有权限作用域'''


class AccountAbstractService(abc.ABC):
    '''账户服务抽象基类'''

    @abc.abstractmethod
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到错误待定义'''

    @abc.abstractmethod
    def recharge(self, account_id: int, value: float) -> model.Account:
        '''充值，并赠送等额积分，返回账户'''


class UserAbstractService(abc.ABC):
    '''用户服务抽象基类'''

    @abc.abstractmethod
    def get_user(self, user_id: int) -> model.User:
        '''获取指定用户，没找到错误待定义'''
    
    @abc.abstractmethod
    def create_user(self, name: str="", phone: str="") -> model.User:
        '''创建用户，并为新用户创建账户，返回携带账户的用户'''


class HealthAbstractService(abc.ABC):
    '''健康检测服务抽象基类'''

    @abc.abstractmethod
    def get_health(self) -> model.Health:
        '''
        返回健康状态。
        包含本地时间、上游服务健康状况
        '''