from django.db import models


class RssFetchSubject(models.Model):

    class Meta:
        db_table = 'fetch_subjects'

    name = models.CharField(max_length=255, null=False, unique=True)
    url = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
