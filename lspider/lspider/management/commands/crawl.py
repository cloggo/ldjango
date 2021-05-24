from django.core.management.base import BaseCommand

from lspider.lspider.spiders import ScrollSpider, ViewStateSpider, LoginSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = "Run scrapy spiders"

    def handle(self, *args, **options):
        settings = get_project_settings()
        # print('settings: ' + str(settings.items()))
        process = CrawlerProcess(settings)
        process.crawl(LoginSpider)
        process.crawl(ScrollSpider)
        process.crawl(ViewStateSpider)
        process.start()

        # print("hello, running spiders...")
