from django.db import models


class Author(models.Model):

    class Meta:
        db_table = 'authors'

    name = models.CharField(max_length=255, null=False)
    link = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
