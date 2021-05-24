import scrapy
import json
from scrapy.exceptions import CloseSpider

## Concurrency Issues:
## * Requests are non-blocking asynchronously scheduled
## * Before the response of last page was returned, extra requests were scheduled
## * Next page depends on state of previous page (next_page = True/False)
##
## Solutions:
## * Setting CONCURRENT_REQUESTS = 1
## * Allow extra requests and parsing go to waste
## * using recursion in parse (calling request)
##
## Considerations:
## Parsing concurrent requests would corrupt the condition has_next unless it is locked. Locking
## the condition variable has_next could potentially resulted in deadlock condition
## if not careful and concurrent requests is blocked anyway when the condition variable is locked.
## If implementing locking mechanism, it would essentially become serial processing.
##
## Scrapy is using "twisted" which is using event loop and request is a non-blocking event.
## It is not a true multithread event.
##
## Because return response and parsing of response is bounded time duration, the extra number
## of requests is also bounded.  Therefore, I chose to allow wastings extra requests.

class ScrollSpider(scrapy.Spider):
    name = 'scroll'
    allowed_domains = ['quotes.toscrape.com']
    # custom_settings = {
    #     'CONCURRENT_REQUESTS': 1,
    # }

    def __init__(self, *args, **kwargs):
        super(ScrollSpider, self).__init__(*args, **kwargs)
        self.__has_next = True

    def start_requests(self):
        base_url = 'http://quotes.toscrape.com/api/quotes?page={page_num}'
        page_num = 1
        while self.__has_next:
            url = base_url.format(page_num=page_num)
            req = scrapy.Request(url=url, callback=self.parse)
            page_num = page_num + 1
            yield req


    def parse(self, response):
        res = json.loads(response.text)
        self.__has_next = res['has_next']
        quotes = res['quotes']

        for quote in quotes:
            yield quote
