#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 用户角色关联模型
#
# wencan
# 2019-04-18

import attr
from datetime import datetime

__all__ = ("UserRole", )

@attr.attrs(auto_attribs=True)
class UserRole:
    '''
    用户角色关联模型
    多对多关系
    无需对外输出
    '''
    __tablename__ = "basic_user_role"

    id: int = attr.attr(metadata={"sql": "id;primary_key"})
    user_id: int
    role_id: int
    created_at: datetime
    updated_at: datetime