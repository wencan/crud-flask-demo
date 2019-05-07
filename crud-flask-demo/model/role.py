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
    _permission_list: typing.Sequence[str] = attr.attr(init=False, default=None, metadata={"sql": "-"})
    created_at: datetime = attr.attr(factory=datetime.now)
    updated_at: datetime = attr.attr(factory=datetime.now)


    # 原计划使用__attrs_post_init__实现。但当对象__init__未被调用时，__attrs_post_init__不会被执行
    # 改用property实现
    @property
    def permission_list(self):
        if self._permission_list is None:
            self._permission_list = self.permissions.split(";")
        return self._permission_list