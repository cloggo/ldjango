# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from .scroll import ScrollSpider
from .viewstate import ViewStateSpider
from .login import LoginSpider

__all__ = [ScrollSpider, ViewStateSpider, LoginSpider]
