import aiohttp_jinja2
import aiohttp
import asyncio
from .urls import url_1, url_3, url_2


async def find_weather_1(session, url):
   async with session.get(url, headers={'Accept': 'application/json', }) as response:
      html = await response.json()
      temp = html['temperature']
      speed = html['wind']
      description = html['description']
      return temp, speed, description


async def find_weather_2(session, url):
   async with session.get(url, headers={'Accept': 'application/json', }) as response:
      html = await response.json()
      temp = str(float("{0:.1f}".format(html['consolidated_weather'][0]['the_temp'])))
      speed = str(float("{0:.1f}".format(html['consolidated_weather'][0]['wind_speed'])))
      description = html['consolidated_weather'][0]['weather_state_name']
      return temp, speed, description


async def find_weather_3(session, url):
   async with session.get(url) as response:
      html = await response.text()
      temp = html.split('\x1b')[5].split('m')[1]
      speed = html.split('\x1b')[14].split('m')[1]
      description = html.split('\x1b')[2].split('m ')[1]
      return temp, speed, description


async def start_async():
   async with aiohttp.ClientSession() as session:
      result1, result2, result3 = await asyncio.gather(find_weather_1(session, url_1), find_weather_2(session, url_2),
                                                       find_weather_3(session, url_3))
   return result1, result2, result3


@aiohttp_jinja2.template("index.html")
async def index(request):
   result1, result2, result3 = await start_async()
   return {'result1': result1, 'result2': result2, 'result3': result3}
