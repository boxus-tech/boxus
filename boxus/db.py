import yaml
from contextlib import contextmanager

import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DB_LINK = "postgresql+psycopg2://localhost/boxus"

engine = create_engine(DB_LINK)
Session = sessionmaker(bind=engine, expire_on_commit=True)

@contextmanager
def db_session_scope():
    """Provide a transactional scope around a series of operations."""

    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print("db_session_scope exception caught: {}".format(repr(e)))
        raise
    finally:
        session.close()

def db_execute(clause, params=None, mapper=None, bind=engine, **kwargs):
    with db_session_scope() as session:
        return session.execute(clause, params, mapper, bind, **kwargs)
