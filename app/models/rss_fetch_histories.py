from django.db import models
from app.models.rss_fetch_subjects import RssFetchSubject


class RssFetchHistory(models.Model):

    class Meta:
        db_table = 'rss_fetch_histories'

    rss_fetch_subject = models.ForeignKey(
        RssFetchSubject,
        related_name='rss_fetch_histories',
        related_query_name='rss_fetch_history',
        on_delete=models.CASCADE,
    )
    date = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    @classmethod
    def exists(cls, rss_fetch_subject_id, date):
        return bool(cls.objects.filter(
            rss_fetch_subject_id=rss_fetch_subject_id,
            date=date,
        ).first())
