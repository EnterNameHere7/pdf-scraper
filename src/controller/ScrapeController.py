import logging
import threading

import jsonpickle
from logging import Logger
from typing import Dict, Optional
import time
import requests
from bs4 import BeautifulSoup

from src.constants.RedisConstants import RedisConstants
from src.model.RedisMessage import RedisMessage
from src.services.PdfService import PdfService
from src.services.RedisService import RedisService
from src.utilities.UrlUtilities import UrlUtilities


class ScrapeController:

    def __init__(self,
                 redis_service: RedisService,
                 config: Dict[str, Optional[str]]
                 ) -> None:
        self.logger = logging.getLogger("scraper")
        self.redis_service = redis_service
        self.config = config

    def start_scraping(self):
        self.logger.info("starting with : {}".format(self.config.get("SCRAPER_URL")))
        self.scrape_page(0, self.config.get("SCRAPER_URL"), self.config.get("SCRAPER_URL"),
                         self.config.get("SCRAPER_DOMAIN"))

    def scrape_page(self, num: int, previous_url: str, incommingUrl: str, domain: str):
        try:

            if num >= int(self.config.get("SCRAPER_LEVEL_LIMIT")):
                return
            else:
                num = num + 1

            url = UrlUtilities.fix_url(previous_url, incommingUrl, domain)

            if self.redis_service.exists(key=RedisConstants.KEY_VISITED.value, value=url):
                return
            else:
                self.redis_service.add_set(key=RedisConstants.KEY_VISITED.value, value=url)

            if num != 1:
                self.logger.info("{} working with : [ {} | {} ] coming from {}".format(num, incommingUrl, url, previous_url))

            read = requests.get(url)
            html_content = read.content
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all anchor tags on the site
            anchor_list = soup.find_all('a')
            for a in anchor_list:
                href = a.get('href')

                # print("{} {}".format(anchor_list.index(a), href))

                if href is None:
                    continue

                if href == "/" or href == "./":
                    continue
                if "http" in href:
                    # Need to make sure it doesn't start crawling other domains
                    if domain not in href:
                        continue

                # print("{} ============> {}".format(url, href))
                if ".pdf" in href:
                    if not self.redis_service.exists(key=RedisConstants.KEY_PDF_DONE.value, value=href):
                        self.redis_service.add_set(key=RedisConstants.KEY_PDF_DONE.value, value=href)

                        fixed_anchor = UrlUtilities.fix_url(previous_url, href, domain)
                        self.logger.info("{} adding : {} ".format(num, fixed_anchor))
                        #PdfService.download_pdf(fixed_anchor)
                        x = threading.Thread(target=PdfService.download_pdf, args=(fixed_anchor,))
                        x.start()
                elif "mailto" in href:
                    # this is an email not interested in this atm
                    continue
                elif "tel:" in href:
                    # this is a telephone number not interested in this atm
                    continue
                else:
                    fixed_anchor = UrlUtilities.fix_url(previous_url, href, domain)
                    if not self.redis_service.exists(key=RedisConstants.KEY_VISITED.value, value=fixed_anchor):
                        self.redis_service.publish(channel=RedisConstants.CHANNEL_UNVISITED.value,
                                                   message=jsonpickle.encode(RedisMessage(num, previous_url, href, domain)))


                # else:
                #     print("{} {} not supported".format(num, href))
        except Exception as e:
            self.logger.info("{} something went wrong".format(num))
            # self.logger.error(e)
        finally:
            self.logger.debug("done with {}".format(self.config.get("SCRAPER_URL")))

