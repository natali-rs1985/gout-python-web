from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database import SessionLocal
import models
import schemas

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/news/", response_model=schemas.AllNews)
def get_all_news(db: Session = Depends(get_db)):
    res = db.query(models.News).all()
    print(res)
    all_news = [
        schemas.News(
            news_id=r.news_id,
            sport=r.sport,
            news=r.news,
            url=r.url,
            time=r.time
        )
        for r in res
    ]
    return schemas.AllNews(all_news=all_news)


@app.get("/news/{news_id}", response_model=schemas.News)
def get_news(news_id: str, db: Session = Depends(get_db)):
    res = db.query(models.News).filter_by(news_id=news_id).first()
    news = schemas.News(
            news_id=res.news_id,
            sport=res.sport,
            news=res.news,
            url=res.url,
            time=res.time
    )
    return news


@app.delete("/news/{news_id}", status_code=204)
def delete_news(news_id: str, db: Session = Depends(get_db)):
    news = db.query(models.News).filter_by(news_id=news_id).first()
    db.delete(news)
    db.commit()


@app.post("/news/", status_code=201, response_model=schemas.News)
def add_author(news: schemas.NewsBase, db: Session = Depends(get_db)) -> schemas.News:
    body = news
    n = models.News()
    n.news = body.news
    n.url = body.url
    n.time = body.time
    n.sport = body.sport
    db.add(n)
    db.commit()
    news_id = db.query(models.News).filter_by(news=body.news).first().news_id
    res = db.query(models.News).filter_by(news_id=news_id).first()
    res_news = schemas.News(
        news_id=res.news_id,
        sport=res.sport,
        news=res.news,
        url=res.url,
        time=res.time
    )
    return res_news
