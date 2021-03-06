from bs4 import BeautifulSoup


class ArxivXml(object):

    @classmethod
    def read_as_bs4(cls, text, parser='xml'):
        return BeautifulSoup(text, parser)

    def __init__(self, xml_text):
        self.root = self.read_as_bs4(xml_text)

    def get_date(self):
        date = self.root.find('dc:date')
        return date.string if date else None

    def _parse_paper_item(self, item_bs):
        title = item_bs.find('title').string.strip()

        description_bs = self.read_as_bs4(
            item_bs.find('description').string.replace('\n', ' '),
            parser='lxml',
        )
        abstract = '\n'.join([p.getText().strip() for p in description_bs.find_all('p')])

        link = item_bs.find('link').string.strip()

        creator_bs = self.read_as_bs4(
            item_bs.find('dc:creator').string.replace('\n', ' '),
            parser='lxml',
        )
        authors = []
        for a in creator_bs.find_all('a'):
            authors.append({
                'name': a.string,
                'link': a.get('href'),
            })

        return {
            'title': title,
            'abstract': abstract,
            'link': link,
            'authors': authors,
        }

    def get_paper_items(self):
        return [self._parse_paper_item(item) for item in self.root.find_all('item')]
