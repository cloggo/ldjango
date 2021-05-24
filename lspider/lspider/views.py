from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AuthorSerializer, TagSerializer, QuoteSerializer

from .models import Author, Tag, Quote

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Author.objects.order_by('id').all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Tag.objects.order_by('id').all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class QuoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Quote.objects.order_by('id').all()
    serializer_class = QuoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'authors': reverse('authors', request=request, format=format),
#         'quotes': reverse('snippet-list', request=request, format=format)
#     })
