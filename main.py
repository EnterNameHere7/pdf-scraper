import logging
import sys
import threading

import flask
import redis
from dotenv import dotenv_values

from src.constants.RedisConstants import RedisConstants
from src.controller.ScrapeController import ScrapeController
from src.router.router import Router
from src.services.RedisService import RedisService
from src.suscribers.ScrapeSubscriber import ScrapeSubscriber

logging.basicConfig(filename="scraper.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

app = flask.Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))

# load configs from .env file
config = dotenv_values(".env")

# initialise publisher redis
redis_service = RedisService(redis.Redis(host=config.get("REDIS_HOST"), db=0))

controller = ScrapeController(app.logger, redis_service, config)

# initialise subscriber redis
subscriber = ScrapeSubscriber(app.logger, RedisConstants.CHANNEL_UNVISITED.value, redis.Redis(host=config.get("REDIS_HOST"), db=0), controller)

for i in range(5):
    x = threading.Thread(target=subscriber.start_subscriber, args=())
    x.start()


Router(app, controller)

app.run()



@app.teardown_appcontext
def shutdownhandler(app):
    redis_service.rem_key(key=RedisConstants.KEY_VISITED.value)

