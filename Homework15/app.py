from fastapi import FastAPI
from starlette.responses import RedirectResponse
import json

from database import SessionLocal
import models
import schemas

app = FastAPI()


def _get_news_by_id(news_id):
    with SessionLocal() as db:
        news_dict = {}
        n = db.query(models.News).filter_by(news_id=news_id).first()
        news_dict['news_id'] = n.news_id
        news_dict['sport'] = n.sport
        news_dict['news'] = n.news
        news_dict['url'] = n.url
        news_dict['time'] = n.time
    news_json = json.dumps(news_dict)
    return news_json


def _get_all_news():
    with SessionLocal() as db:
        news = db.query(models.News).all()
        news_list = []
        for n in news:
            news_dict = {}
            news_dict['news_id'] = n.news_id
            news_dict['sport'] = n.sport
            news_dict['news'] = n.news
            news_dict['url'] = n.url
            news_dict['time'] = n.time
            news_list.append(news_dict)
        news_json = json.dumps(news_list)
    return news_json


def _add_news(body):
    with SessionLocal() as db:
        n = models.News()
        n.news = body['news']
        n.url = str(body['url'])
        n.time = body['time']
        n.sport = body['sport']
        db.add(n)
        db.commit()
        news_id = db.query(models.News).filter_by(news=n.news).first().news_id
    return news_id


def _delete_news(news_id):
    with SessionLocal() as db:
        news = db.query(models.News).filter_by(news_id=news_id).first()
        db.delete(news)
        db.commit()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/news/", status_code=200, response_model=schemas.AllNews)
def get_all_news():
    res = _get_all_news()
    res = json.loads(res)
    all_news = [schemas.News(**r) for r in res]
    return schemas.AllNews(all_news=all_news)


@app.get("/news/{news_id}", status_code=200, response_model=schemas.News)
def get_news(news_id: str):
    res = _get_news_by_id(news_id)
    res = json.loads(res)
    news = schemas.News(**res)
    return news


@app.delete("/news/{news_id}", status_code=204)
def delete_news(news_id: str):
    _delete_news(news_id)
    return


@app.post("/news/", status_code=201, response_model=schemas.News)
def add_news(news: schemas.NewsBase) -> schemas.News:
    body = news.dict()
    news_id = _add_news(body)
    res = _get_news_by_id(news_id)
    res = json.loads(res)
    res_news = schemas.News(**res)
    return res_news
