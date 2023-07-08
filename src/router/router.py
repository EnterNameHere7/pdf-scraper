import flask

from src.controller.ScrapeController import ScrapeController


class Router:

    def __init__(self,
                 app: flask.Flask,
                 scrape_controller: ScrapeController
                 ) -> None:


        @app.route("/", methods=['GET', 'POST'])
        def default():
            return "WOOPSIE"

        @app.route("/start", methods=['GET'])
        def startScraping():
            scrape_controller.start_scraping()
            return "started"