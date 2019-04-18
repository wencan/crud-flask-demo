#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户的用户名和密码
#
# wencan
# 2019-04-18

import attr
from datetime import datetime

__all__ = ("BasicAuthorization", )

@attr.attrs(auto_attribs=True)
class BasicAuthorization:
    '''
    用户账户模型
    '''
    __tablename__ = "basic_authorization"

    id: int = attr.attr(default=None, metadata={"sql": "id;primary_key"})
    user_id: int = attr.attr(default=None)
    username: str = attr.attr(default=0)
    password: str = attr.attr(default=0)
    created_at: datetime = attr.attr(default=None)
    updated_at: datetime = attr.attr(default=None)