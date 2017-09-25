import json
from django import template
from app.lib.util.json_encoder import OriginalJSONEncoder

register = template.Library()


@register.filter
def to_json(value):
    return json.dumps(value, ensure_ascii=False, cls=OriginalJSONEncoder)
