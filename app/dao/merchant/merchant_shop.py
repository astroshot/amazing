# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import VARCHAR, TIMESTAMP, BIGINT, TINYINT, TEXT

from app.db import DAO, use_session
from app.define import Status


class MerchantShopDAO(DAO):
    __tablename__ = 'merchant_shop'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    merchant_id = Column(BIGINT)
    name = Column(VARCHAR(64), doc=u'merchant shop name')
    description = Column(VARCHAR(1024), doc=u'merchant shop phone')
    address = Column(TEXT, doc=u'address of merchant shop')
    status = Column(TINYINT, doc=u'merchant status', default=Status.NORMAL.value)
    contanct_info = Column(TEXT, doc=u'contract info, in json format')
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, name, description, address, contanct_info, status=Status.NORMAL.value):
        shop = cls(name=name, description=description, address=address, contanct_info=contanct_info, status=status)
        cls.session.add(shop)
        cls.session.commit()
        return shop.id
