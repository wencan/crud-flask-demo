#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 账户模型
#
# wencan
# 2019-04-13

import attr
from datetime import datetime

__all__ = ("Account", )

@attr.attrs(auto_attribs=True)
class Account:
    '''
    用户账户模型
    '''
    __tablename__ = "basic_account"

    id: int = attr.attr(metadata={"sql": "id;primary_key"})
    balance: float
    score: float
    created_at: datetime
    updated_at: datetime