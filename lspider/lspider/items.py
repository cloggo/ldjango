# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem

from .models import Author, AuthorSlug, Tag, LinkType, AuthorLink, Quote, QuoteStatus, QuoteTag


class AuthorItem(DjangoItem):
    django_model = Author


class AuthorSlugItem(DjangoItem):
    django_model = AuthorSlug


class TagItem(DjangoItem):
    django_model = Tag


class LinkTypeItem(DjangoItem):
    django_model = LinkType


class AuthorLinkItem(DjangoItem):
    django_model = AuthorLink


class QuoteItem(DjangoItem):
    django_model = Quote


class QuoteStatusItem(DjangoItem):
    django_model = QuoteStatus


class QuoteTagItem(DjangoItem):
    django_model = QuoteTag
