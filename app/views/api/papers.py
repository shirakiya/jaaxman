from datetime import datetime

from aws_xray_sdk.core import xray_recorder
from django.http import JsonResponse
from django.views.decorators.http import require_GET

import app.lib.util.xray as xrayutil
from app.views.helpers import (
    fetch_papers_with_date,
    fetch_papers_with_offset,
    fetch_papers_with_query,
    filter_papers_with_query,
    format_jsonable_date_to_papers,
)


@xray_recorder.capture('view.api.paper')
@require_GET
def api_papers(request):
    segment = xrayutil.current_segment()

    params = request.GET

    date = params.get('date')
    query = params.get('query')
    offset = int(params.get('count', 0))

    segment.put_metadata('date', date, 'request')
    segment.put_metadata('query', query, 'request')
    segment.put_metadata('count', offset, 'request')

    if date:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            papers = fetch_papers_with_date(date)
        except ValueError:
            papers = []
        papers = filter_papers_with_query(papers, query)
    elif query:
        papers = fetch_papers_with_query(query)
    else:
        papers = fetch_papers_with_offset(offset)

    return JsonResponse({
        'papers': format_jsonable_date_to_papers(papers),
    })
