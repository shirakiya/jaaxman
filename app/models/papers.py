from django.db import models
from app.models.rss_fetch_histories import RssFetchHistory


class Paper(models.Model):

    class Meta:
        db_table = 'papers'

    rss_fetch_history = models.ForeignKey(
        RssFetchHistory,
        related_name='papers',
        related_query_name='paper',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255, null=False)
    title_ja = models.CharField(max_length=255, null=False)
    abstract = models.TextField(null=False)
    abstract_ja = models.TextField(null=False)
    link = models.TextField(null=False)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
