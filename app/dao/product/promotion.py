# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import TIMESTAMP, BIGINT, TINYINT, INTEGER

from app.db import DAO, use_session


class PromotionDAO(DAO):
    __tablename__ = 'promotion'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    sku_id = Column(BIGINT)
    price = Column(INTEGER, doc=u'sku price')
    is_promotion = Column(TINYINT, doc=u'是否促销')
    promotion_price = Column(INTEGER, doc=u'sku promotion price')
    start_time = Column(BIGINT, doc=u'促销开始时间')
    end_time = Column(BIGINT, doc=u'促销结束时间')
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, sku_id, price, is_promotion, promotion_price, start_time, end_time):
        promotion = cls(sku_id=sku_id, price=price, is_promotion=is_promotion, promotion_price=promotion_price,
                        start_time=start_time, end_time=end_time)
        cls.session.add(promotion)
        cls.session.commit()
        return promotion.id
