# coding=utf-8
from sqlalchemy import Column, func
from sqlalchemy.dialects.mysql import TIMESTAMP, BIGINT, TEXT

from app.db import DAO, use_session


class FeedbackDAO(DAO):
    __tablename__ = 'feedback'

    id = Column(BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(BIGINT)
    info = Column(TEXT, doc=u'feedback detail, json format')
    created_at = Column(TIMESTAMP, doc=u'创建时间', default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, doc=u'修改时间', default=func.current_timestamp(), onupdate=func.current_timestamp())

    @classmethod
    @use_session(master=True)
    def add(cls, user_id, info):
        feedback = cls(user_id=user_id, info=info)
        cls.session.add(feedback)
        cls.session.commit()
        return feedback.id
