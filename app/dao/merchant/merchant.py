# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import VARCHAR, TIMESTAMP, BIGINT, TINYINT

from app.db import DAO, use_session
from app.define import Status


class MerchantDAO(DAO):
    __tablename__ = 'merchant'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(64), doc=u'user name')
    description = Column(VARCHAR(1024), doc=u'phone')
    status = Column(TINYINT, doc=u'merchant status', default=Status.NORMAL.value)
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, name, description, status=Status.NORMAL.value):
        merchant = cls(name=name, description=description, status=status)
        cls.session.add(merchant)
        cls.session.commit()
        return merchant.id
