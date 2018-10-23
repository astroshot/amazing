# coding=utf-8
from itertools import cycle

import logging
import threading
from contextlib import contextmanager
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.util import ObjectDict

from app.config import db_conf

_g = threading.local()

mysql_master = create_engine(
    db_conf['master'], echo=db_conf['echo_sql'],
    pool_size=2, max_overflow=48,
    pool_timeout=0, pool_recycle=3600)

mysql_slaves = [
    create_engine(
        slave_db_connect_string, echo=db_conf['echo_sql'],
        pool_size=6, max_overflow=48,
        pool_timeout=0, pool_recycle=300)
    for slave_db_connect_string in db_conf['slaves']]

MasterSession = sessionmaker(bind=mysql_master)
SlaveSessions = cycle([sessionmaker(bind=slave) for slave in mysql_slaves])


# Be sure to close slave sessions before async call.
# It's also recommend to close master sessions at that time.


def get_session(master=False, autocommit=False, autoflush=True):
    if getattr(_g, 'using_master', None):
        _using_master = True
    else:
        _using_master = master

    if _using_master:
        return MasterSession(autocommit=autocommit, autoflush=autoflush)
    else:
        # slave always autocommit
        return next(SlaveSessions)(autocommit=True, autoflush=autoflush)


def _format_obj_dict(dao, data):
    from app.db import DAO

    if not isinstance(dao, type):
        return data

    if not issubclass(dao, DAO):
        return data

    if data is None:
        return

    if isinstance(data, dao):
        return dao.format_obj_dict(data)
    elif isinstance(data, tuple):
        return [_format_obj_dict(dao, item) for item in data]
    elif isinstance(data, list):
        return [_format_obj_dict(dao, item) for item in data]
    elif isinstance(data, dict):
        return ObjectDict((key, _format_obj_dict(dao, value)) for key, value in data)
    else:
        return data


def use_session(func=None, master=False, auto_commit=False, auto_flush=False):
    _inject_attr_name = 'session'

    def wrap(func):
        @wraps(func)
        def inner(*args, **kwargs):
            pre_session = None
            is_injected = False
            session = None
            global_session = getattr(_g, _inject_attr_name, None)

            if hasattr(args[0], _inject_attr_name):  # session has been injected
                is_injected = True
                pre_session = getattr(args[0], _inject_attr_name, None)

                if pre_session.bind == mysql_master and global_session is None:
                    session = pre_session

            if session is None:
                session = global_session or get_session(master, auto_commit, auto_flush)
                setattr(args[0], _inject_attr_name, session)

            transaction = session.begin(True) if global_session else session.transaction

            try:
                result = func(*args, **kwargs)
                result = _format_obj_dict(args[0], result)
                if session.bind == mysql_master and transaction.is_active:
                    transaction.commit()
            except Exception as e:
                raise e
            finally:
                if is_injected:
                    setattr(args[0], _inject_attr_name, pre_session)
                else:
                    delattr(args[0], _inject_attr_name)
                if not global_session:
                    session.close()
            return result

        return inner

    if func is None:
        return wrap
    else:
        return wrap(func)


@contextmanager
def using_master():
    """
    `using_master` decorator forces `get_session` and `use_session` bind to master database
    >>> with using_master:
    >>>     session = get_session()
    >>>     session.query(...)
    """
    _old = None

    try:
        _old = getattr(_g, 'using_master', None)
        _g.using_master = True
        logging.debug('using master...')
        yield
    finally:
        if _old is None:
            del _g.using_master
        else:
            _g.using_master = _old
        del _old
        logging.debug('end using master...')


@contextmanager
def using_global_transaction():
    """
    `using_global_transaction` decorator forces `get_session` returns Master `session(master=True)`,
    and ignore config in `use_session`
    used to construct transaction
    >>> from app.dao.user import UserDAO
    >>> with using_global_transaction() as session:
    >>>     try:
    >>>         UserDAO.add(name='name', phone_no='+861xxxxxxxxx', email='email@xxx.com')
    >>>         session.commit()
    >>>     except:
    >>>         session.rollback()
    """
    _old_session = None

    try:
        _old_session = getattr(_g, 'session', None)
        _g.session = get_session(master=True)
        logging.debug('using global master session...')
        yield _g.session
        _g.session.commit()
    except:
        _g.session.rollback()
        raise
    finally:
        _g.session.close()
        if _old_session is None:
            del _g.session
        else:
            _g.session = _old_session
        del _old_session
        logging.debug('end using global master session...')
