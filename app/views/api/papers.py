from django.http import JsonResponse
from django.views.decorators.http import require_GET
from app.views.helpers import create_jsonable_papers


@require_GET
def api_papers(request):
    params = request.GET
    offset = int(params['count'])

    jsonable_papers = create_jsonable_papers(offset)

    return JsonResponse({
        'papers': jsonable_papers,
    })
