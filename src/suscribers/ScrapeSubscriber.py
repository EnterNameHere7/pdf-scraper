from logging import Logger

import jsonpickle
from redis.client import Redis

from src.constants.RedisConstants import RedisConstants
from src.controller.ScrapeController import ScrapeController


class ScrapeSubscriber:

    def __init__(self,
                 logger: Logger,
                 channel: str,
                 redis: Redis,
                 scrape_controller: ScrapeController) -> None:
        self.logger = logger
        self.redis = redis
        self.channel = channel
        self.scrape_controller = scrape_controller

    def start_subscriber(self):
        self.logger.info("starting listener")
        subscriber = self.redis.pubsub()

        subscriber.subscribe(self.channel)

        self.logger.info("starting waiting for messages on {}".format(self.channel))
        for message in subscriber.listen():
            try:
                if message["data"] is not 1:
                    self.handle_message(message["data"])
            except:
                # do nothing
                self.logger.debug("woopsie")


    def handle_message(self, message: str):
        try:
            redis_message = jsonpickle.decode(message)
            self.logger.debug("subscriber IN {}".format(message))
            self.scrape_controller.scrape_page(num=redis_message.num, previous_url=redis_message.previous_url,
                                               url=redis_message.url, domain=redis_message.domain)

            self.redis.sadd(RedisConstants.KEY_DONE.value, redis_message.url)
        except Exception as e:
            self.logger.info(e)
