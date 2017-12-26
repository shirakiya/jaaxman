from django.http import JsonResponse
from django.views.decorators.http import require_GET
from app.views.helpers import (
    create_jsonable_date_to_papers_with_offset,
    create_jsonable_date_to_papers_with_date,
)


@require_GET
def api_papers(request):
    params = request.GET

    date = params.get('date')
    offset = params.get('count', 0)

    if date:
        jsonable_date_to_papers = create_jsonable_date_to_papers_with_date(date)
    else:
        jsonable_date_to_papers = create_jsonable_date_to_papers_with_offset(int(offset))

    return JsonResponse({
        'papers': jsonable_date_to_papers,
    })
