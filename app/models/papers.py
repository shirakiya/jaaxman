import re
from django.db import models
from jaaxman.logger import Logger
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
    subject = models.CharField(max_length=255, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def set_subject(self):
        match = re.search(r'\(.*\[(.+)\].*\)', self.title)
        if not match:
            Logger.warn(f"Could not extract paper's subject. title => {self.title}")
            self.subject = ''
            return False
        else:
            self.subject = match.groups()[0]
            return True

    def set_translation(self):
        self.title_ja = 'タイトル(仮)'
        self.abstract_ja = '要約(仮)'

    def add_authors(self, authors_dict):
        pass
