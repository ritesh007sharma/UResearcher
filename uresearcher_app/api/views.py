from django.shortcuts import render
from rest_framework import generics
from .serializers import ArticleSerializer
from .models import Article

# Create your views here.
class ArticleView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

