from typing import List

from pydantic import BaseModel, AnyHttpUrl


class NewsBase(BaseModel):

    news: str
    url: AnyHttpUrl
    time: str
    sport: str


class News(NewsBase):
    news_id: str


class AllNews(BaseModel):
    all_news: List[News]

