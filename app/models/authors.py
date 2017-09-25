from django.db import models


class Author(models.Model):

    class Meta:
        db_table = 'authors'

    name = models.CharField(max_length=255, null=False)
    link = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def dumps(self):
        return {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
