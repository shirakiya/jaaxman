from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from app.models import Paper


@require_GET
def api_paper(request, paper_id):
    try:
        paper = Paper.objects\
            .prefetch_related('rss_fetch_history')\
            .prefetch_related('authors')\
            .get(pk=paper_id)
    except Paper.DoesNotExist as e:
        raise Http404(e)

    paper_dump = paper.dumps()
    paper_dump['rss_fetch_subject_id'] = paper.rss_fetch_history.rss_fetch_subject_id

    return JsonResponse(paper_dump)
