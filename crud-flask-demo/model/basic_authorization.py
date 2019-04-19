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

    id: int = attr.attr(metadata={"sql": "id;primary_key"})
    user_id: int
    username: str
    password: str
    created_at: datetime
    updated_at: datetime