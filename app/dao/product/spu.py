# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import VARCHAR, TIMESTAMP, BIGINT, TINYINT, TEXT

from app.db import DAO, use_session
from app.define import Status


class SpuDAO(DAO):
    __tablename__ = 'spu'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    url_token = Column(VARCHAR(64), doc=u'spu url_token')
    name = Column(VARCHAR(64), doc=u'spu name')
    description = Column(VARCHAR(1024), doc=u'spu description')
    image_hash = Column(VARCHAR(256), doc=u'spu image')
    business = Column(TINYINT, doc=u'spu business', default=0)  # not used yet
    status = Column(TINYINT, doc=u'spu status', default=Status.NORMAL.value)
    merchant_id = Column(BIGINT)
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, name, description, image_hash, url_token, category_id,
            business, merchant_id=0, status=Status.NORMAL.value):
        spu = cls(name=name, description=description, image_hash=image_hash, url_token=url_token,
                  category_id=category_id, business=business, merchant_id=merchant_id, status=status)
        cls.session.add(spu)
        cls.session.commit()
        return spu.id
