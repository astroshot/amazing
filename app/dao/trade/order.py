# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import VARCHAR, TIMESTAMP, BIGINT, TINYINT, INTEGER, TEXT

from app.db import DAO, use_session


class OrderDAO(DAO):
    __tablename__ = 'order'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BIGINT)
    trade_token = Column(VARCHAR(64), doc=u'trade token')
    sales_amount = Column(INTEGER(11), doc=u'卖价')
    pay_amount = Column(INTEGER(11), doc=u'买价')
    status = Column(TINYINT, doc=u'user type, 0 consumer 1 merchant')
    snapshot = Column(TEXT, doc=u'交易快照， json 格式')
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, user_id, trade_token, sales_amount, pay_amount, status, snapshot):
        order = cls(user_id=user_id, trade_token=trade_token, sales_amount=sales_amount, pay_amount=pay_amount,
                    status=status, snapshot=snapshot)
        cls.session.add(order)
        cls.session.commit()
        return order.id

    @classmethod
    @use_session
    def get(cls, id):
        query = cls.session.query(cls).filter(cls.id == id)
        return query.one_or_none()
