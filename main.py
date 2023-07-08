import logging
import os
import threading
import time
import urllib.request

import requests
from bs4 import BeautifulSoup

list_of_pdf = list()
list_of_visited = list()

limit = 100

logging.basicConfig(filename="scraper.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('urbanGUI')


def fix_url(previous_url: str, url: str, domain: str):
    if domain not in url:
        # this means it's trying to use relative paths lets fix them

        if url.startswith("../"):
            if previous_url.endswith("/"):
                previous_url = previous_url[:-1]

            url = previous_url[:previous_url.rfind('/')] + "/" + url.replace("../", "")
        elif url.startswith("/"):
            url = domain + url
        elif url.startswith("#"):
            raise ValueError("Url can't start with a #")
        elif "/" not in url:
            if ".html" in previous_url:
                url = previous_url[:previous_url.rfind('/')] + "/" + url
            else:
                url = previous_url.rstrip("/") + "/" + url
        else:
            if not url.startswith("http"):
                if ".html" in previous_url:
                    url = previous_url[:previous_url.rfind('/')] + "/" + url
                else:
                    url = previous_url.rstrip("/") + "/" + url
            else:
                url = previous_url + url
    return url


def scrape_page(num, previous_url, url, domain):
    try:
        if num >= limit:
            return
        else:
            num = num + 1

        if url in list_of_visited:
            return

        time.sleep(0.5)
        url = fix_url(previous_url, url, domain)
        list_of_visited.append(url)

        logger.info("{} working with : {} coming from {}".format(num, url, previous_url))

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
                fixed_anchor = fix_url(previous_url, href, domain)
                logger.info("{} adding : {} ".format(num, fixed_anchor))
                download_pdf(0, fixed_anchor)
            elif "mailto" in href:
                # this is an email not interested in this atm
                continue
            else:
                fixed_anchor = fix_url(previous_url, href, domain)
                if fixed_anchor not in list_of_visited:
                    # scrape_page(num, url, href, domain)
                    x = threading.Thread(target=scrape_page, args=(num, url, href, domain))
                    x.start()
                    # x.join()

            # else:
            #     print("{} {} not supported".format(num, href))
    except Exception as e:
        logger.info("{} something went wrong".format(num))
        logger.error(e)

def download_pdf(index, pdf_path):
    folder_path = "./downloads"

    folder_path = os.path.join(folder_path, pdf_path.split('/')[-2])
    if not os.path.exists(folder_path): os.mkdir(folder_path)
    file_save_path = os.path.join(folder_path, pdf_path.split('/')[-1])

    if os.path.exists(file_save_path):
        file_save_path = file_save_path + "(" + index + ")"

    urllib.request.urlretrieve(pdf_path, file_save_path)


domain = "http://www.saflii.org"
url = "http://www.saflii.org/content/databases"
scrape_page(0, url, url, domain)

# list_of_pdf.append("http://www.saflii.org/images/CJdecision.pdf")

for i in list_of_pdf:
    try:
        print("downloading {} out of {}".format(list_of_pdf.index(i), len(list_of_pdf)))
        download_pdf(list_of_pdf.index(i), i)
    except:
        print("something went wrong downloading file " + i)
