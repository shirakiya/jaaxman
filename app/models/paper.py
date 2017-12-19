from logging import getLogger
import re
from django.db import models
from app.models.rss_fetch_history import RssFetchHistory
from app.models.author import Author
from app.lib.google_translator import GoogleTranslator

logger = getLogger(__name__)


class Paper(models.Model):

    class Meta:
        db_table = 'papers'

    rss_fetch_history = models.ForeignKey(
        RssFetchHistory,
        related_name='papers',
        related_query_name='paper',
        on_delete=models.CASCADE,
    )
    authors = models.ManyToManyField(
        Author,
        related_name='papers',
        related_query_name='paper',
    )
    title = models.CharField(max_length=255, null=False)
    title_ja = models.CharField(max_length=255, null=False)
    abstract = models.TextField(null=False)
    abstract_ja = models.TextField(null=False)
    link = models.TextField(null=False)
    subject = models.CharField(max_length=255, blank=True, null=False)
    submit_type = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    SUBMIT_TYPE_NEW = 'new'
    SUBMIT_TYPE_UPDATED = 'updated'
    SUBMIT_TYPE_CROSS_LISTED = 'cross_listed'
    SUBMIT_TYPES = (
        (SUBMIT_TYPE_NEW, 'NEW'),
        (SUBMIT_TYPE_UPDATED, 'UPDATED'),
        (SUBMIT_TYPE_CROSS_LISTED, 'CROSS LISTED'),
    )

    @classmethod
    def from_xml(cls, arxiv_paper_item):
        self = cls(
            title=arxiv_paper_item['title'],
            abstract=arxiv_paper_item['abstract'],
            link=arxiv_paper_item['link'],
        )
        self._set_subject()
        self.set_submit_type()
        self._set_translation()
        return self

    def _set_subject(self):
        match = re.search(r'\(.*\[(.+)\].*\)', self.title)
        if not match:
            logger.warn(f"Could not extract paper's subject. title => {self.title}")
            self.subject = ''
            return False
        else:
            self.subject = match.groups()[0]
            return True

    def set_submit_type(self):
        for submit_type, submit_type_title in self.SUBMIT_TYPES:
            if self.title.endswith(f'{submit_type_title})'):
                self.submit_type = submit_type
        if not self.submit_type:
            self.submit_type = self.SUBMIT_TYPE_NEW
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

    def add_authors(self, authors_from_xml):
        authors = []
        for author_dict in authors_from_xml:
            author = Author.objects.create(
                name=author_dict['name'],
                link=author_dict['link'],
            )
            authors.append(author)
        if not authors:
            return False
        self.authors.add(*authors)
        return True

    def dumps(self):
        return {
            'id': self.id,
            'title': self.title,
            'title_ja': self.title_ja,
            'abstract': self.abstract,
            'abstract_ja': self.abstract_ja,
            'link': self.link,
            'subject': self.subject,
            'submit_type': self.submit_type,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'authors': [author.dumps() for author in self.authors.all()],
        }
