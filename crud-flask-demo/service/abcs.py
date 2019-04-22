#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# cmd/rest 抽象基类集合
# wencan
# 2019-04-14

import abc
import typing

from .. import model

__all__ = (
            "AccountRequiredAccountAbstractCrud",
            "UserRequiredAccountAbstractCrud",
            "AccountAbstractCrud", 
            "UserAbstractCrud", 
            "BasicAuthorizationAbstractCrud", 
            "RoleAbstractCrud", 
            "UserRoleAbstractCrud",
            "HealthAbstractCrud", 
            "NoRowsAbstractException")


class NoRowsAbstractException(Exception):
    '''crud not_found 异常抽象基类'''
    pass


class AccountRequiredAccountAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到返回None'''

    @abc.abstractmethod
    def add_balance(self, account_id: int, value: float):
        '''充值，返回账户'''

    @abc.abstractmethod
    def add_score(self, account_id: int, value: float):
        '''加积分，返回账户'''

class UserRequiredAccountAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def create_account(self, balance: float=0, score: float=0) ->model.Account:
        '''创建并返回新账户'''

    @abc.abstractmethod
    def get_account(self, account_id: int) -> model.Account:
        '''获得指定账户，没找到返回None'''


class AccountAbstractCrud(AccountRequiredAccountAbstractCrud, UserRequiredAccountAbstractCrud):
    pass


class UserAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def create_user(self, account_id: int, name: str = "", phone: str = "") -> model.User:
        '''创建并返回新账户'''

    @abc.abstractmethod
    def get_user(self, account_id) -> model.User:
        '''获得指定用户，没找到返回None'''
 

class BasicAuthorizationAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def verify_username_password(self, username: str, password: str) -> int:
        '''验证用户名和密码，成功返回用户id，否则抛出NoRows'''

class RoleAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def get_role(self, role_id: int) -> model.Role:
        '''获得指定角色信息（含权限信息）'''


class UserRoleAbstractCrud(abc.ABC):
    @abc.abstractmethod
    def get_roles_by_user(self, user_id: int) -> typing.Iterable[int]:
        '''获得关联到指定用户的角色。即使没关联到角色也返回空序列'''

class HealthAbstractCrud(abc.ABC):
    '''数据库的健康检测'''

    @abc.abstractmethod
    def get_health(self) -> model.Health:
        '''返回各个数据库的时间信息'''