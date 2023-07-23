from enum import Enum


class RedisConstants(Enum):
    KEY_VISITED = "URL:VISITED"
    KEY_DONE = "URL:DONE"
    KEY_UNVISITED = "URL:UNVISITED"

    KEY_PDF_DONE = "PDF:DONE"

    CHANNEL_UNVISITED = "URL_UNVISITED"
