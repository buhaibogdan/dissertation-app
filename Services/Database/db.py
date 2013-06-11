from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from conf.conf import mysql_issueManagerDB

engine = create_engine(mysql_issueManagerDB, convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class DB(object):
    @staticmethod
    def init():
        Base.metadata.create_all(bind=engine)


