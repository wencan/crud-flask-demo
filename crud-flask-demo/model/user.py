#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户模型
#
# wencan
# 2019-04-12

import attr
from datetime import datetime

from .account import Account

__all__ = ("User", )


@attr.attrs(auto_attribs=True)
class User:
    '''
    用户模型
    '''
    __tablename__ = "basic_user"

    id: int = attr.attr(default=None, metadata={"sql": "id;primary_key"})
    name: str = attr.attr(default="", metadata={"sql": "user_name"})
    phone: str = attr.attr(default="", metadata={"sql": "mobile"})
    account_id: int = attr.attr(default=None, metadata={"sql": "account_id", "json": "-"})
    account: Account = attr.attr(default=None, converter=lambda d: Account(**d), metadata={"sql": "-"})
    created_at: datetime = attr.attr(default=None)
    updated_at: datetime = attr.attr(default=None)

    # def __attrs_post_init__(self):
    #     # 从account推导account_id
    #     if self.account_id is None and self.account is not None and self.account.id is not None:
    #         self.account_id = self.account.id

