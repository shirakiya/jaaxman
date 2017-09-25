import json
from datetime import datetime


class OriginalJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super(OriginalJSONEncoder, self).default(obj)
