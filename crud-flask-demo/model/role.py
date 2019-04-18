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

    id: int = attr.attr(default=None, metadata={"sql": "id;primary_key"})
    name: str = attr.attr(default="", metadata={"sql": "role_name"})
    permissions: str = attr.attr(default="")
    # permission_list: typing.Iterable[str] = attr.attr(init=False, metadata={"sql": "-"})
    created_at: datetime = attr.attr(default=None)
    updated_at: datetime = attr.attr(default=None)

    # 测试发现__attrs_post_init__未被执行
    # def __attrs_post_init__(self):
    #     self.permission_list = self.permissions.split(";")