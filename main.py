import logging
import sys

import flask
import redis
from dotenv import dotenv_values

from src.controller.ScrapeController import ScrapeController
from src.router.router import Router
from src.services.RedisService import RedisService

logging.basicConfig(filename="scraper.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = flask.Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))

# load configs from .env file
config = dotenv_values(".env")

# initialise redis
r = redis.Redis(host=config.get("REDIS_HOST"), db=0)
redis_service = RedisService(r)

controller = ScrapeController(app.logger, redis_service, config)

Router(app, controller)

app.run()

