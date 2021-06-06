from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.TextField(null=False)
    abstract = models.TextField(null=True)
    abstract_formatted = models.TextField(null=True)
    fulltext = models.TextField(null=True)
    doi = models.TextField(null=True)
    eid = models.TextField(null=True)
    link = models.TextField(null=True)
    publisher = models.TextField(null=True)
    publish_date = models.TextField(null=True)
    keywords = models.TextField(null=True) 




    