import requests
import unicodedata
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import News, Base
from src.config import config


SQLALCHEMY_DATABASE_URL = config["postgres"]["url"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def parse_data_kyiv():
    news_ = []
    url = 'https://vechirniy.kyiv.ua/'
    html_doc = requests.get(url)
    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        all_news = soup.find('ul', attrs={'class': 'most-important'}).find_all('li')
        for news in all_news:
            title = unicodedata.normalize("NFKD", news.find('span', class_="title").text)
            text = None
            category = 'Kyiv'
            link_short = news.find('a')["href"]
            link = f'{url[:-1]}{link_short}'
            news_.append({
                'title': title,
                'text': text,
                'category': category,
                'link': link
            })
    return news_


def parse_data_ottawa():
    news_ = []
    url = 'https://www.cbc.ca/news/canada/ottawa'
    html_doc = requests.get(url)
    if html_doc.status_code == 200:
        soup = BeautifulSoup(html_doc.content, 'html.parser')
        all_news = soup.find('div', attrs={'class': 'contentListCards', 'data-test': 'topStories'}).find_all('a', attrs={'data-test': 'type-story'})
        for news in all_news:
            title = news.find('h3', class_="headline").text
            text = None
            try:
                text = unicodedata.normalize("NFKD", news.find('div', class_="description").text)
            except AttributeError:
                pass
            category = 'Ottawa'
            link_short = news["href"]
            link = f'{url}{link_short}'
            news_.append({
                'title': title,
                'text': text,
                'category': category,
                'link': link
            })
    return news_


def fill_db():
    news = parse_data_kyiv() + parse_data_ottawa()
    news_db = Session()
    for el in news:
        news_record = News(title=el.get('title'), text=el.get('text'), category=el.get('category'), link=el.get('link'))
        news_db.add(news_record)
    news_db.commit()
    news_db.close()


def get_db():
    news_db = Session()
    try:
        yield news_db
    finally:
        news_db.close()


if __name__ == "__main__":
    fill_db()
