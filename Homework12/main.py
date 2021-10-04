from aiohttp import web
import jinja2
import aiohttp_jinja2


def setup_routes(application):
   from app.weather.routes import setup_routes as setup_forum_routes
   setup_forum_routes(application)


def setup_external_libraries(application: web.Application) -> None:
   aiohttp_jinja2.setup(application, loader=jinja2.FileSystemLoader("templates"))


def setup_app(application):
   setup_external_libraries(application)
   setup_routes(application)


app = web.Application()


if __name__ == "__main__":
   setup_app(app)
   web.run_app(app, host='localhost')
