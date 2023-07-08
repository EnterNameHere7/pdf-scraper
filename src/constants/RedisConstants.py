from enum import Enum


class RedisConstants(Enum):
    KEY_VISITED = "URL:VISITED"
    KEY_DONE = "URL:DONE"
    KEY_UNVISITED = "URL:UNVISITED"

    CHANNEL_UNVISITED = "URL_UNVISITED"
