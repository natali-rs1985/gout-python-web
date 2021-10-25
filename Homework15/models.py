from sqlalchemy import Column, Integer, String

from database import Base


class News(Base):
    __tablename__ = "news"

    news_id = Column(Integer, primary_key=True, index=True)
    news = Column(String, unique=True)
    url = Column(String, unique=True)
    time = Column(String)
    sport = Column(String)

