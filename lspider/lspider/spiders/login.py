import scrapy
import json
from scrapy.exceptions import CloseSpider
# from urllib import urlencode
from scrapy.http import FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def login_status(self, response):
        logout = response.xpath('//a[@href="/logout"]/text()').get()
        if logout is None:
            raise CloseSpider('Login was unsuccessful.')

    def parse(self, response):
        # extract csrf_token
        # csrf_token = 'x'
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        username = 'a'
        password = 'b'

        params = {
            'csrf_token': csrf_token,
            'username': username,
            'password': password
        }

        yield scrapy.FormRequest(url=LoginSpider.start_urls[0],
                                 formdata=params,
                                 callback=self.login_status)
