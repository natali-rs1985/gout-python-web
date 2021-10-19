# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy.orm import sessionmaker
from .models import QuoteDB, AuthorDB, TagDB, db_connect, create_table


class QuotesSpyderPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        quotedb = QuoteDB(quote=item["quote"])
        authordb = AuthorDB()
        authordb.name = item["author"]

        exist_author = session.query(AuthorDB).filter_by(name=item["author"]).first()
        if exist_author:
            quotedb.author = exist_author
        else:
            quotedb.author = authordb

        authordb.url = item["author_url"][0]
        authordb.birthday = item['author_birthday']
        authordb.location = item['author_location']
        authordb.info = item['author_info']

        if "tags" in item:
            for tag in item["tags"]:
                tag = TagDB(tag=tag)
                exist_tag = session.query(TagDB).filter_by(tag=tag.tag).first()
                if exist_tag:
                    tag = exist_tag
                quotedb.tags.append(tag)

        try:
            session.add(quotedb)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
