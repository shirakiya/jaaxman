from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from app.views.helpers import (
    fetch_papers_with_date,
    fetch_papers_with_offset,
    fetch_papers_with_query,
    filter_papers_with_query,
    format_jsonable_date_to_papers,
)


@require_GET
def api_papers(request):
    params = request.GET

    date = params.get('date')
    query = params.get('query')

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
        offset = params.get('count', 0)
        papers = fetch_papers_with_offset(int(offset))

    return JsonResponse({
        'papers': format_jsonable_date_to_papers(papers),
    })
