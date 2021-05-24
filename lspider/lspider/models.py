from django.db import models

import django.utils.timezone as tz


class Author(models.Model):
    name = models.CharField(max_length=156, unique=True)


class AuthorSlug(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=156)


class Tag(models.Model):
    tag = models.CharField(max_length=156, unique=True)


class LinkType(models.Model):
    type = models.CharField(max_length=156)


class AuthorLink(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    link_type = models.ForeignKey(LinkType, on_delete=models.CASCADE)
    link = models.CharField(max_length=156)


class Quote(models.Model):
    author = models.ForeignKey(Author, related_name='quotes', on_delete=models.CASCADE)
    created_at = models.DateTimeField('quote created at', default=tz.now)
    updated_at = models.DateTimeField('quote updated at', default=tz.now)
    quote = models.TextField(max_length=512, unique=True)


class QuoteStatus(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created_at = models.DateTimeField('status created at', default=tz.now)
    status = models.BooleanField(default=True)


class AuthorTag(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class QuoteTag(models.Model):
    quote = models.ForeignKey(Quote, related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='quotes', on_delete=models.CASCADE)
