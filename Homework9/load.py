from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def view(self, *args):
        pass


class ViewerInterface(Interface):
    def view(self, *args):
        print(*args)


Base = declarative_base()
CONNECTION_STRING_ASSISTANT = 'postgresql://postgres:1051985qaz@localhost/assistant'


engine = create_engine(CONNECTION_STRING_ASSISTANT)
metadata = Base.metadata
DBSession = sessionmaker(bind=engine)
session = DBSession()


viewer = ViewerInterface().view


