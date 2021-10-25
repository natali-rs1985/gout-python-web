from database import Base, engine, SessionLocal
from news import news_1, news_2
from models import News


def create_news_1(session):
    all_news = news_1()
    for news in all_news:
        n = News()
        n.time = news['time']
        n.url = news['url']
        n.news = news['news']
        n.sport = news['sport']
        try:
            session.add(n)
            session.commit()
        except:
            session.rollback()
            raise


def create_news_2(session):
    all_news = news_2()
    for news in all_news:
        n = News()
        n.time = news['time']
        n.url = news['url']
        n.news = news['news']
        n.sport = news['sport']
        try:
            session.add(n)
            session.commit()
        except:
            session.rollback()
            raise


def create_all():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal()as session:
        create_news_1(session)
        create_news_2(session)


if __name__ == '__main__':
    create_all()

