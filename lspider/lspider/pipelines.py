# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem

from django.db import IntegrityError

from lspider.lspider.models import Author, AuthorSlug, LinkType, AuthorLink, Tag, Quote, QuoteTag, QuoteStatus, AuthorTag


def get_author_link(item):
    return next(((k, v) for k, v in item.items() if k.endswith('link')), (None,None))

class LspiderAuthorPipeline:
    def process_item(self, item, spider):
        item_ = item['author']

        author_name = item_['name']

        if author_name is None:
            raise DropItem('not a valid author')

        author = Author.objects.filter(name=author_name).first()

        if author is None:
            author = Author(name=item_['name'])
            author.save()

        txt = item_.get('slug')
        if txt:
            slug = AuthorSlug(author=author, slug=txt)
            slug.save()

        k, v = get_author_link(item_)

        if k is None:
            return item

        link_type = LinkType.objects.filter(type=k).first()

        if link_type is None:
            link_type = LinkType(type=k)
            link_type.save()

        link = AuthorLink(author=author, link_type=link_type, link=v)
        link.save()

        return item


class LspiderTagPipeline:
    def process_item(self, item, spider):
        for tag in item.get('tags', []):
            is_exist = Tag.objects.filter(tag=tag).exists()

            if is_exist:
                continue

            tag = Tag(tag=tag)
            tag.save()

        return item


class LspiderQuotePipeline:
    def process_item(self, item, spider):
        author = Author.objects.filter(name=item['author']['name']).first()
        quote = Quote.objects.filter(author=author, quote=item['text']).first()

        if quote:
            return item

        quote = Quote(author=author, quote=item['text'])
        quote.save()

        quote_status = QuoteStatus(quote=quote)
        quote_status.save()

        for tag in item.get('tags', []):
            tag = Tag.objects.filter(tag=tag).first()
            quote_tag = QuoteTag(quote=quote, tag=tag)

            quote_tag.save()

            author_tag = AuthorTag(author=author, tag=tag)
            author_tag.save()

        return item
