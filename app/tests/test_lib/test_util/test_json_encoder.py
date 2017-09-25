import json
from datetime import datetime
from app.tests.base_testcase import BaseTestCase
from app.lib.util.json_encoder import OriginalJSONEncoder


class OriginalJSONEncoderTestCase(BaseTestCase):

    def dumps(self, value):
        return json.dumps(value, cls=OriginalJSONEncoder)

    def test_dumps_datetime(self):
        verified = {
            'value': datetime.strptime('2017/09/01 12:00:00.100000', '%Y/%m/%d %H:%M:%S.%f'),
        }
        result = self.dumps(verified)

        self.assertEqual(result, '{"value": "2017-09-01T12:00:00.100000"}')

    def test_dumps_set(self):
        verified = {
            'value': set([1, 2]),
        }
        result = self.dumps(verified)

        self.assertEqual(result, '{"value": [1, 2]}')
