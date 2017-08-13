from app.tests.creations import (
    CreationRssFetchHistory,
    CreationRssFetchSubject,
    CreationPaper,
)


class Creation(object):

    def __init__(self):
        self.rss_fetch_history = CreationRssFetchHistory()
        self.rss_fetch_subject = CreationRssFetchSubject()
        self.paper = CreationPaper()
