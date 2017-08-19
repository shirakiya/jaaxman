import re
from django.db import models
from jaaxman.logger import Logger
from app.models.rss_fetch_histories import RssFetchHistory
from app.lib.google_translator import GoogleTranslator


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

    @classmethod
    def from_xml(cls, arxiv_paper_item):
        self = cls(
            title=arxiv_paper_item['title'],
            abstract=arxiv_paper_item['abstract'],
            link=arxiv_paper_item['link'],
        )
        self._set_subject()
        self._set_translation()
        return self

    def _set_subject(self):
        match = re.search(r'\(.*\[(.+)\].*\)', self.title)
        if not match:
            Logger.warn(f"Could not extract paper's subject. title => {self.title}")
            self.subject = ''
            return False
        else:
            self.subject = match.groups()[0]
            return True

    def _set_translation(self):
        texts = [
            self.title,
            self.abstract,
        ]
        translated_texts = GoogleTranslator.translate(texts)
        if len(translated_texts) != 2:
            return False
        self.title_ja = translated_texts[0]
        self.abstract_ja = translated_texts[1]
        return True

    def add_authors(self, authors_dict):
        pass
