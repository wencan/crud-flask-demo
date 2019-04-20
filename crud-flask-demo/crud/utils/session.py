#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# sqlalchemy会话辅助
#
# wencan
# 2019-04-20

import typing
from contextlib import contextmanager

from sqlalchemy.orm import Session, sessionmaker as SessionMaker, scoped_session as ScopedSession


__all__ = ("scoped_session_maker")


def scoped_session_maker(session_factory: typing.Callable[..., Session]) -> typing.Callable[[], typing.ContextManager[Session]]:
    '''
    sqlalchemy会话上下文工厂函数，支持嵌套事务
    支持下层抛出异常，整个事务回滚
    但有一个缺陷：在上层抛出异常，不会回滚
    
    sqlalchemy的scoped_session支持同一个maker同一个线程/协程返回同一个session
    '''

    session_maker = ScopedSession(session_factory=session_factory)

    @contextmanager
    def scoped_session(subtransactions_supported: bool=False) -> typing.Iterator[Session]:
        '''
        sqlalchemy会话上下文
        subtransactions_supported = True，表示为一个嵌套事务的外层上下文
        '''

        session = session_maker()
        try:
            if subtransactions_supported:
                session.begin(subtransactions=subtransactions_supported)

            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            # session.expunge_all() # 从会话中移除所有查询到的对象
            if subtransactions_supported:
                session.close()
    
    return scoped_session