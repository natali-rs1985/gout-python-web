from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, Text)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)


quote_tag_table = Table(
    'quote_tag',
    metadata,
    Column('quote_id', ForeignKey('quote.quote_id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tag.tag_id', ondelete='CASCADE'), primary_key=True)
)


class QuoteDB(DeclarativeBase):
    __tablename__ = "quote"

    quote_id = Column(Integer, primary_key=True)
    quote = Column('quote', Text())
    author_id = Column(Integer, ForeignKey('author.author_id', ondelete='CASCADE'))
    tags = relationship('TagDB', secondary=quote_tag_table, back_populates='quote', cascade='all, delete')
    author = relationship('AuthorDB', back_populates='quote', cascade='all, delete')


class AuthorDB(DeclarativeBase):
    __tablename__ = 'author'

    author_id = Column(Integer, primary_key=True)
    name = Column('name', String(100), unique=True)
    url = Column('url', String(100))
    birthday = Column('birthday', Date)
    location = Column('born location', String(100))
    info = Column('information', Text())
    quote = relationship('QuoteDB', back_populates='author')


class TagDB(DeclarativeBase):
    __tablename__ = 'tag'

    tag_id = Column(Integer, primary_key=True)
    tag = Column('tag', String(100), unique=True)
    quote = relationship('QuoteDB', secondary=quote_tag_table, back_populates='tags')
