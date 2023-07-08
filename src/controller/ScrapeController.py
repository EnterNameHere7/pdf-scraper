import threading
from logging import Logger
from typing import Dict, Optional
import time
import requests
from bs4 import BeautifulSoup

from src.services.PdfService import PdfService
from src.services.RedisService import RedisService
from src.utilities.UrlUtilities import UrlUtilities


class ScrapeController:

    def __init__(self,
                 logger: Logger,
                 redis_service: RedisService,
                 config: Dict[str, Optional[str]]
                 ) -> None:
        self.logger = logger
        self.redis_service = redis_service
        self.config = config

    def start_scraping(self):

        print("here")
        print(self.config.get("SCRAPER_URL"))

        self.logger.info("starting with : {}".format(self.config.get("SCRAPER_URL")))
        self.scrape_page(0, self.config.get("SCRAPER_URL"), self.config.get("SCRAPER_URL"),
                         self.config.get("SCRAPER_DOMAIN"))

    def scrape_page(self, num: int, previous_url: str, url: str, domain: str):
        try:

            if num >= int(self.config.get("SCRAPER_LEVEL_LIMIT")):
                return
            else:
                num = num + 1

            self.logger.info(self.redis_service.exists(key="URL:VISITED", value=url))

            if self.redis_service.exists(key="URL:VISITED", value=url):
                return

            time.sleep(0.5)
            url = UrlUtilities.fix_url(previous_url, url, domain)
            self.redis_service.add_set(key="URL:VISITED", value=url)

            if num != 1:
                self.logger.info("{} working with : {} coming from {}".format(num, url, previous_url))

            read = requests.get(url)
            html_content = read.content
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all anchor tags on the site
            anchor_list = soup.find_all('a')
            for a in anchor_list:
                href = a.get('href')

                print("{} {}".format(anchor_list.index(a), href))

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
                    fixed_anchor = UrlUtilities.fix_url(previous_url, href, domain)
                    self.logger.info("{} adding : {} ".format(num, fixed_anchor))
                    PdfService.download_pdf(fixed_anchor)
                elif "mailto" in href:
                    # this is an email not interested in this atm
                    continue
                else:
                    if not self.redis_service.exists(key="URL:VISITED", value=url):
                        # scrape_page(num, url, href, domain)
                        x = threading.Thread(target=self.scrape_page, args=(num, url, href, domain))
                        x.start()
                        # x.join()

                # else:
                #     print("{} {} not supported".format(num, href))
        except Exception as e:
            self.logger.info("{} something went wrong".format(num))
            self.logger.error(e)
