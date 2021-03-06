#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 健康状况
#
# wencan
# 2019-04-17

import attr
from datetime import datetime

__all__ = ("Health", )


@attr.attrs(auto_attribs=True)
class Health:
    '''健康状况'''

    mysql_time: datetime

    server_time: datetime = attr.attr(factory=datetime.now)