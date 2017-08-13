from bs4 import BeautifulSoup
from app.tests.base_testcase import BaseTestCase
from app.lib.xml.arxiv import ArxivXml


class ArxivXmlTestCase(BaseTestCase):

    def setUp(self):
        self.dummy_xml = '<rdf:RDF></rdf:RDF>'

    def test_read_as_bs4(self):
        result = ArxivXml.read_as_bs4(self.get_arxiv_xml())

        self.assertIsInstance(result, BeautifulSoup)

    def test_get_date(self):
        arxiv_xml = ArxivXml(self.get_arxiv_xml())
        result = arxiv_xml.get_date()

        self.assertEqual(result, '2017-08-10T20:30:00-05:00')

    def test_get_date_when_not_exists(self):
        arxiv_xml = ArxivXml(self.dummy_xml)
        result = arxiv_xml.get_date()

        self.assertEqual(result, None)

    def test_parse_paper_item(self):
        item_bs = ArxivXml.read_as_bs4('''
<item rdf:about="http://arxiv.org/abs/1708.00000" xmlns:dc="http://purl.org/dc/elements/1.1/">
<title>
TITLE (arXiv:1708.00000 [cs.HC])
</title>
<link>http://arxiv.org/abs/1708.00000</link>
<description rdf:parseType="Literal">
&lt;p&gt;DESCRIPTION_0&lt;/p&gt;&lt;p&gt;DESCRIPTION_1\nDESCRIPTION_2&lt;/p&gt;
</description>
<dc:creator> &lt;a href="http://arxiv.org/find/stat/1/1"&gt;CREATOR_0&lt;/a&gt;, &lt;a href="http://arxiv.org/find/stat/1/2"&gt;CREATOR_1&lt;/a&gt;</dc:creator>
</item>
        '''.strip())  # noqa: E501

        arxiv_xml = ArxivXml(self.dummy_xml)
        result = arxiv_xml._parse_paper_item(item_bs)

        self.assertEqual(result['title'], 'TITLE (arXiv:1708.00000 [cs.HC])')
        self.assertEqual(result['abstract'], 'DESCRIPTION_0\nDESCRIPTION_1 DESCRIPTION_2')
        self.assertEqual(result['link'], 'http://arxiv.org/abs/1708.00000')
        self.assertEqual(result['authors'], [
            {
                'name': 'CREATOR_0',
                'link': 'http://arxiv.org/find/stat/1/1',
            },
            {
                'name': 'CREATOR_1',
                'link': 'http://arxiv.org/find/stat/1/2',
            },
        ])

    def test_get_paper_items(self):
        arxiv_xml = ArxivXml('''
<rdf:RDF xmlns:dc="http://purl.org/dc/elements/1.1/">
<item rdf:about="LINK_0">
<title>
TITLE_0
</title>
<link>LINK_0</link>
<description rdf:parseType="Literal">
&lt;p&gt;DESCRIPTION_0&lt;/p&gt;
</description>
<dc:creator> &lt;a href="CREATOR_LINK_0"&gt;CREATOR_0&lt;/a&gt;</dc:creator>
</item>
<item rdf:about="LINK_1">
<title>
TITLE_1
</title>
<link>LINK_1</link>
<description rdf:parseType="Literal">
&lt;p&gt;DESCRIPTION_1&lt;/p&gt;
</description>
<dc:creator> &lt;a href="CREATOR_LINK_1"&gt;CREATOR_1&lt;/a&gt;</dc:creator>
</item>
</rdf:RDF>
        '''.strip())
        result = arxiv_xml.get_paper_items()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['paper'].title, 'TITLE_0')
        self.assertEqual(result[0]['paper'].abstract, 'DESCRIPTION_0')
        self.assertEqual(result[0]['paper'].link, 'LINK_0')
        self.assertEqual(result[0]['authors'], [{'name': 'CREATOR_0', 'link': 'CREATOR_LINK_0'}])
        self.assertEqual(result[1]['paper'].title, 'TITLE_1')
        self.assertEqual(result[1]['paper'].abstract, 'DESCRIPTION_1')
        self.assertEqual(result[1]['paper'].link, 'LINK_1')
        self.assertEqual(result[1]['authors'], [{'name': 'CREATOR_1', 'link': 'CREATOR_LINK_1'}])
