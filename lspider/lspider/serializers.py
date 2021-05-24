from rest_framework import serializers

from .models import Author, Tag, Quote

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    quotes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='quote-detail'
    )

    class Meta:
        model = Author
        fields = ['id', 'url', 'name', 'quotes']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    quotes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='quote-detail'
    )

    class Meta:
        model = Tag
        fields = ['id', 'url', 'tag', 'quotes']


class QuoteSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    tags = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='tag-detail'
    )

    class Meta:
        model = Quote
        fields = ['id', 'url', 'created_at', 'updated_at', 'author', 'quote', 'tags']

