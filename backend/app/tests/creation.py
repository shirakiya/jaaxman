from app.tests.creations import CreationAuthor, CreationPaper, CreationRssFetchHistory, CreationRssFetchSubject


class Creation(object):

    def __init__(self):
        self.rss_fetch_history = CreationRssFetchHistory()
        self.rss_fetch_subject = CreationRssFetchSubject()
        self.paper = CreationPaper()
        self.author = CreationAuthor()
