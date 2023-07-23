class RedisMessage(object):
    num = int
    previous_url = str
    url = str
    domain = str

    def __init__(self, num: int, previous_url: str, url: str, domain: str):
        self.num = num
        self.previous_url = previous_url
        self.url = url
        self.domain = domain
