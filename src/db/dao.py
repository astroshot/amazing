# coding=utf-8

from sqlalchemy import MetaData, func
from sqlalchemy.ext.declarative import declarative_base
from tornado.util import ObjectDict

from src.db.session import mysql_master, use_session

_DAO = declarative_base()


class DAO(_DAO):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'extend_existing': True,
    }

    metadata = MetaData(bind=mysql_master, reflect=False)

    def to_obj_dict(self, hidden_fields=None):
        _fields = ['_sa_instance_state']
        if isinstance(hidden_fields, (list, tuple)):
            hidden_fields = list(_fields + hidden_fields)
        else:
            hidden_fields = _fields

        obj_dict = ObjectDict((k, v) for k, v in self.__dict__.items() if k not in hidden_fields)
        return obj_dict

    @classmethod
    def format_obj_dict(cls, instance):
        if instance is None:
            return
        elif isinstance(instance, cls):
            return instance.to_obj_dict()
        else:
            raise TypeError

    @classmethod
    def get_columns(cls):
        return cls.__table__.columns.keys()

    @classmethod
    @use_session
    def get_by_unique_attr(cls, attr_name, attr_value, columns=None, lock_mode=None):
        attr = getattr(cls, attr_name)
        if attr:
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = cls.session.query(*columns)
                else:
                    scalar = True
                    query = cls.session.query(columns)
            else:
                query = cls.session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(attr == attr_value)
            if scalar:
                return query.scalar()
            return query.first()

    @classmethod
    @use_session
    def get_by_unique_attrs(cls, attr_name, attr_values, columns=None, lock_mode=None):
        if attr_values:
            attr = getattr(cls, attr_name)
            if attr:
                if columns:
                    if isinstance(columns, (tuple, list)):
                        query = cls.session.query(*columns)
                    else:
                        query = cls.session.query(columns)
                else:
                    query = cls.session.query(cls)
                if lock_mode:
                    query = query.with_lockmode(lock_mode)
                query = query.filter(attr.in_(attr_values))
                return query.all()
        else:
            # attr_values are empty
            pass
        return []

    @classmethod
    def get_by_id(cls, id, columns=None, lock_mode=None):
        return cls.get_by_unique_attr('id', id, columns, lock_mode)

    @classmethod
    def mget_by_ids(cls, ids, columns=None, lock_mode=None):
        return cls.get_by_unique_attrs('id', ids, columns, lock_mode)

    @classmethod
    def mget_by_unique_attrs(cls, attr_name, attr_values):
        results = [None] * len(attr_values)
        query_result = cls.get_by_unique_attrs(attr_name, filter(None, attr_values), None)
        result_mapping = {getattr(item, attr_name): item for item in query_result}
        for i, value in enumerate(attr_values):
            results[i] = result_mapping.get(value)
        return results

    @classmethod
    @use_session(master=True)
    def delete_by_id(cls, id):
        obj = cls.session.query(cls).filter(cls.id == id).scalar()
        cls.session.delete(obj)
        cls.session.commit()

    @classmethod
    @use_session
    def exist(cls, id):
        if hasattr(cls, 'id'):
            query = cls.session.query('1').select_from(cls).filter(cls.id == id)
            return query.scalar() is not None
        return False

    @classmethod
    @use_session
    def count(cls, **kwargs):
        return cls.session.query(func.count(cls.id)).filter_by(**kwargs).scalar()

    @classmethod
    @use_session(master=True)
    def update(cls, id, update_vals):
        row_count = cls.session.query(cls).filter_by(id=id).update(values=update_vals)
        cls.session.commit()
        return row_count > 0
