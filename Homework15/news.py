import requests
from bs4 import BeautifulSoup

URL_1 = 'https://ua.tribuna.com/news'
URL_2 = 'https://new.sport.ua/'

trans = {
    'футбол': 'football',
    'хоккей': 'hockey',
    'теннис': 'tennis',
    'баскетбол': 'basketball',
    'авто/мото': 'automoto',
    'биатлон': 'biathlon',
    'бокс': 'boxing',
    'футзал': 'soccer',
    'тяжелая атлетика': 'heavyathletics',
    'худ.гимнастика': 'gymnastics',
    'киберспорт': 'betting',
    'другие виды': 'others',
    'спортивная гимнастика': 'gymnastics',
    'легкая атлетика': 'athletics',
    'формула 1': 'automoto',
    'гандбол': 'handball',
    'шахматы': 'chess',
    'другие новости': 'others',
    'борьба': 'wrestling',
    }


def news_2(url_2=URL_2):
    news_list = []
    html = requests.get(url_2).text
    soup = BeautifulSoup(html, 'html.parser')
    inf = soup.find('div', {'class', 'news'}).find_all('div', {'class', 'item'})
    for i in inf:
        news = {}
        news['time'] = i.find('span', {'class', 'item-date'}).text.strip()
        sport = i.find('div', {'class', 'item-row'}).find('span').text.casefold()
        news['sport'] = trans.get(sport, sport)
        news['url'] = i.find('a').get('href')
        news['news'] = i.find('div', {'class', 'item-title'}).text.strip()
        news_list.append(news)

    return news_list


def news_1(url_1=URL_1):
    news_list = []
    html = requests.get(url_1).text
    soup = BeautifulSoup(html, 'html.parser')
    inf = soup.find('div', {'class': 'short-news'}).find_all('p')
    for i in inf:
        news = {}
        news['time'] = i.find('span', {'class', 'time'}).text.strip()
        inf = i.find('a')
        news['sport'] = inf.get('href').split('/')[1]
        news['url'] = url_1 + inf.get('href')
        news['news'] = inf.text.strip()
        news_list.append(news)
    return news_list
