from datetime import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False, unique=False)
    created = Column(DateTime, default=datetime.now())
    text = Column(String(2000), nullable=True, unique=False)
    category = Column(String(50), nullable=False, unique=False)
    link = Column(String(500), nullable=False, unique=True)

