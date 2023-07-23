import logging
import urllib.parse

import requests
from requests.utils import requote_uri
import os
import urllib.request


class PdfService:

    @staticmethod
    def download_pdf(pdf_path: str):
        logger = logging.getLogger("scraper")

        pdf_path = urllib.parse.unquote(pdf_path)

        try:
            download_folder = "downloads"
            if not os.path.exists(download_folder): os.mkdir(download_folder)

            folder_path = os.path.join(download_folder, pdf_path.split('/')[-2])
            if not os.path.exists(folder_path): os.mkdir(folder_path)

            file_save_path = os.path.join(folder_path, pdf_path.split('/')[-1])

            pdf_path = requote_uri(pdf_path)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            with open(file_save_path, "wb") as file:
                response = requests.get(pdf_path, headers=headers)
                file.write(response.content)
        except Exception as e:
            logger.error("COULD NOT PULL : {}".format(pdf_path))
        finally:
            return
