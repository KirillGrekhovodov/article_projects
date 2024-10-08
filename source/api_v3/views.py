from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v2.serializers import ArticleSerializer
from api_v2.serializers.article import ArticleShortSerializer, CommentSerializer
from webapp.models import Article


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = []
    # pagination_class = PageNumberPagination
    # page_size = 10

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     return Response({"test": "test"})

    # def get_queryset(self):
    #     return Article.objects.filter(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleShortSerializer
        return ArticleSerializer

    #http://localhost:8000/api/v3/articles/1/get_comments_count/
    @action(methods=['GET'], detail=True, url_path='comments')
    def get_comments(self, request, *args, **kwargs):
        return Response(CommentSerializer(self.get_object().comments.all(), many=True).data)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        return Response({'status': 'ok'})


