import scrapy
import json
from scrapy.http import FormRequest
import functools

class ViewStateSpider(scrapy.Spider):
    name = 'viewstate'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/search.aspx']
    filter_url = 'http://quotes.toscrape.com/filter.aspx'

    def __init__(self, *args, **kwargs):
        super(ViewStateSpider,self).__init__(*args, **kwargs)

    def parse_quote(self, response):
        xquote = response.xpath('//div[@class="quote"]')
        quote = xquote.xpath('./span[@class="content"]/text()').get()
        author = xquote.xpath('./span[@class="author"]/text()').get()
        tag = xquote.xpath('./span[@class="tag"]/text()').get()

        yield {'author': {'name': author}, 'tags': [tag], 'text': quote}

    def search_quote(self, response):
        ## selected author and tag state
        vs = ViewStateSpider.__parse_viewstate(response)
        # vs = self.__parse_viewstate(response)
        author = response.xpath('//*[@id="author"]/option[@selected]/text()').get().strip()
        tag = response.xpath('//*[@id="tag"]/option[@selected]/text()').get().strip()

        # self.log("SELECTED TAG: " + tag)
        formdata = {'author': author,
                    'tag': tag,
                    '__VIEWSTATE': vs,
                    'submit_button': 'Search'}

        # parse quote
        yield scrapy.FormRequest(url=self.filter_url,
                                formdata=formdata,
                                    callback=self.parse_quote)


    # delay request (setting download_delay) required callback to be a member of spider class
    def select_tag(self, response):
        ## selected author state
        vs = ViewStateSpider.__parse_viewstate(response)
        # vs = self.__parse_viewstate(response)
        author = response.xpath('//*[@id="author"]/option[@selected]/text()').get().strip()

        # self.log("SELECTED AUTHOR: " + author)
        xres = response.xpath('//*[@id="tag"]/option/text()')
        tags = (tag.extract().strip() for tag in xres)
        # self.log(tags)

        tag0 = next(tags)

        # select tag
        for tag in tags:
            formdata = {'author': author,
                        'tag': tag,
                        '__VIEWSTATE': vs}

            yield scrapy.FormRequest(
                url=self.filter_url,
                formdata=formdata,
                callback=self.search_quote)

    @staticmethod
    def __parse_viewstate(response):
        # self.log("Parsing viewstate")
        return response.xpath('//*[@id="__VIEWSTATE"]/@value').extract()


    def parse(self, response):
        # self.log("Parsing authors")

        ## initial state
        vs = ViewStateSpider.__parse_viewstate(response)

        xres = response.xpath('//*[@id="author"]/option/text()')
        # xres = response.xpath('//*[@id="author"]/option/@value')
        authors = (author.extract().strip() for author in xres)
        # self.log(authors)

        author0 = next(authors)

        # select author
        for author in authors:
            formdata = {'author': author, 'tag': author0, '__VIEWSTATE': vs}
            yield scrapy.FormRequest(url=self.filter_url,
                                     formdata=formdata,
                                     callback=self.select_tag)

