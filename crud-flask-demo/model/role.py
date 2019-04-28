#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 角色模型
# 带权限信息
#
# wencan
# 2019-04-18

import attr
import typing
from datetime import datetime

__all__ = ("Role", )

@attr.attrs(auto_attribs=True)
class Role:
    '''
    角色模型
    无需对外输出
    '''
    __tablename__ = "basic_role"

    id: int = attr.attr(metadata={"sql": "id;primary_key"})
    name: str = attr.attr(metadata={"sql": "role_name"})
    permissions: str
    # permission_list: typing.Sequence[str] = attr.attr(init=False, metadata={"sql": "-"})
    created_at: datetime = attr.attr(factory=datetime.now)
    updated_at: datetime = attr.attr(factory=datetime.now)

    # 测试发现__attrs_post_init__未被执行
    # def __attrs_post_init__(self):
    #     self.permission_list = self.permissions.split(";")