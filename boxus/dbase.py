import json, collections
from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, func,\
                       delete, insert, update, select
from sqlalchemy.ext.declarative import declarative_base

from .db import db_session_scope, db_execute
from .utils import as_list

Base = declarative_base()

class DBase(Base):
    __abstract__ = True

    oid = Column('id', Integer, primary_key=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True))

    # Class methods
    @classmethod
    def delete(cls, oids):
        return db_execute(
            delete(cls).where(cls.oid.in_(as_list(oids)))
        )

    @classmethod
    def find(cls, oids):
        with db_session_scope() as session:
            return session.query(cls).filter(cls.oid.in_(as_list(oids)))

    @classmethod
    def update(cls, oid, attributes):
        return db_execute(
            update(cls, values=attributes).where(cls.oid == oid)
        )

    # Instance methods
    def create(self):
        with db_session_scope() as session:
            return session.add(self)

    def delete(self):
        return __class__.delete(self.oid)

    def update(self, attributes):
        return __class__.update(self.oid, attributes)

    def to_dict(self, filter_keys=None):
        if not filter_keys:
            filter_keys = []

        filter_keys.append('_sa_instance_state')
        result = {}

        for key, value in self.__dict__.items():
            if key not in filter_keys:
                result[key] = value

        return result

    def serialize(self, only=None, filter_keys=None):
        dic = self.to_dict(filter_keys)

        if only:
            dic = { k: dic[k] for k in only }

        return dic

    def to_json(self):
        return json.dumps(self.serialize(), default=str, sort_keys=True)
