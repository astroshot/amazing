# coding=utf-8

from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import VARCHAR, TIMESTAMP, BIGINT

from app.db import DAO, use_session


class UserDAO(DAO):
    __tablename__ = 'user'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(64), doc=u'user name')
    phone_no = Column(VARCHAR(32), doc=u'phone')
    email = Column(VARCHAR(32), doc=u'email')
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, name, phone_no, email):
        user = cls(name=name, phone_no=phone_no, email=email)
        cls.session.add(user)
        cls.session.commit()
        return user.id

    @classmethod
    @use_session
    def get(cls, id):
        query = cls.session.query(cls).filter(cls.id == id)
        return query.one_or_none()
