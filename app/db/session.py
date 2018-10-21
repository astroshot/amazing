# coding=utf-8
from itertools import cycle

import threading
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
            if isinstance(args[0], object):
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
            return func(*args, **kwargs)

        return inner

    if func is None:
        return wrap
    else:
        return wrap(func)
