from django.http import JsonResponse
from django.views.decorators.http import require_GET
from jaaxman.exceptions import InvalidApiParamsError
from app.views.helpers import (
    create_jsonable_date_to_papers_with_offset,
    create_jsonable_date_to_papers_with_date,
)


@require_GET
def api_papers(request):
    params = request.GET

    offset = params.get('count')
    date = params.get('date')

    if offset:
        jsonable_date_to_papers = create_jsonable_date_to_papers_with_offset(int(offset))
    elif date:
        jsonable_date_to_papers = create_jsonable_date_to_papers_with_date(date)
    else:
        raise InvalidApiParamsError('Invalid API params.')

    return JsonResponse({
        'papers': jsonable_date_to_papers,
    })
