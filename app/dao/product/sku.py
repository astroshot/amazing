# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import VARCHAR, TIMESTAMP, BIGINT, TINYINT, INTEGER

from app.db import DAO, use_session
from app.define import Status


class SkuDAO(DAO):
    __tablename__ = 'sku'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    spu_id = Column(BIGINT)
    url_token = Column(VARCHAR(64), doc=u'sku url_token')
    business = Column(TINYINT, doc=u'sku business', default=0)
    image_hash = Column(VARCHAR(256), doc=u'sku image')
    name = Column(VARCHAR(64), doc=u'sku name')
    description = Column(VARCHAR(1024), doc=u'sku description')
    price = Column(INTEGER, doc=u'sku price')
    qrcode_token = Column(VARCHAR(64), doc=u'sku qrcode')
    stock = Column(INTEGER)
    unit = Column(VARCHAR(128), doc=u'sku unit')
    status = Column(TINYINT, doc=u'sku status', default=Status.NORMAL.value)
    merchant_shop_id = Column(BIGINT)
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())
    share_title = Column(VARCHAR(256), doc=u'share title')
    shelf_up_time = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    shelf_down_time = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, spu_id, url_token, business, image_hash, name, description, price, qrcode_token, stock, unit,
            merchant_shop_id, share_title, shelf_up_time, shelf_down_time, status=Status.NORMAL.value):
        sku = cls(spu_id=spu_id, url_token=url_token, business=business, image_hash=image_hash, name=name,
                  description=description, price=price, qrcode_token=qrcode_token, stock=stock, unit=unit,
                  merchant_shop_id=merchant_shop_id, share_title=share_title, shelf_up_time=shelf_up_time,
                  shelf_down_time=shelf_down_time, status=status)
        cls.session.add(sku)
        cls.session.commit()
        return sku.id
