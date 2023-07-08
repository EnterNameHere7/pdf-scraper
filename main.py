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

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = flask.Flask("scraper")
app.logger.addHandler(logging.StreamHandler(sys.stdout))

# load configs from .env file
config = dotenv_values(".env")

# initialise publisher redis
redis_service = RedisService(redis.Redis(host=config.get("REDIS_HOST"), db=0))

controller = ScrapeController(redis_service, config)

# initialise subscriber redis
subscriber = ScrapeSubscriber(RedisConstants.CHANNEL_UNVISITED.value, redis.Redis(host=config.get("REDIS_HOST"), db=0), controller)

subscriber.start_subscriber()

# for i in range(5):
#     x = threading.Thread(target=subscriber.start_subscriber, args=())
#     x.start()


Router(app, controller)

app.run()



@app.teardown_appcontext
def shutdownhandler(app):
    redis_service.rem_key(key=RedisConstants.KEY_VISITED.value)

