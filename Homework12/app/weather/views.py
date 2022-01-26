import aiohttp_jinja2
import aiohttp
import asyncio
from .urls import url_1, url_3, url_2
from datetime import datetime
from bs4 import BeautifulSoup
import re


async def find_weather_1(session, url):
   async with session.get(url) as response:
      html = await response.text()
      soup = BeautifulSoup(html, "html.parser")
      inf = soup.find('div', {'class': "forecast_frame forecast_now"})

      temp = inf.find('span', {'class': "js_value tab-weather__value_l"}).text.strip()
      wind = inf.find('div', {'class': "nowinfo__value"}).text.strip()
      desc = inf.find('span', {'class': "tip _top _center"}).text

      return temp, wind, desc


async def find_weather_2(session, url):
   now = datetime.now().date()
   date = str(now)
   async with session.get(url + date) as response:
      html = await response.text()
      soup = BeautifulSoup(html, "html.parser")

      inf = soup.find('div', {'class': "tabsContent"})

      temp = inf.find('p', {'class': "today-temp"}).text.strip()
      wind = inf.find('div', {'class': "Tooltip wind wind-N"}).text.strip()
      desc = inf.find('div', {'class': re.compile("weatherIco")})['title']

      return temp, wind, desc


async def find_weather_3(session, url):
   async with session.get(url) as response:
      html = await response.text()
      soup = BeautifulSoup(html, "html.parser")
      inf = soup.find('body')

      temp = inf.find('span', {'class': "CurrentConditions--tempValue--3a50n"}).text.strip()
      wind = inf.find('span', {'class': "Wind--windWrapper--3aqXJ undefined"}).text.split('on')[1].split(' ')[0]
      wind = round((int(wind) / 3.6),1)
      desc = inf.find('div', {'class': "CurrentConditions--phraseValue--2Z18W"}).text

      return temp, wind, desc


async def start_async():
   async with aiohttp.ClientSession() as session:
      result1, result2, result3 = await asyncio.gather(find_weather_1(session, url_1), find_weather_2(session, url_2),
                                                       find_weather_3(session, url_3))
   return result1, result2, result3


@aiohttp_jinja2.template("index.html")
async def index(request):
   result1, result2, result3 = await start_async()
   return {'result1': result1, 'result2': result2, 'result3': result3}
