from .models import Article
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title','abstract','abstract_formatted','fulltext','doi','eid','link','publisher','publish_date','keywords')