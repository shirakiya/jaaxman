from aws_xray_sdk.core import xray_recorder
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_GET

import app.lib.util.xray as xrayutil
from app.models import Paper


@xray_recorder.capture('view.api.paper')
@require_GET
def api_paper(request, paper_id):
    segment = xrayutil.current_segment()
    segment.put_metadata('paper_id', paper_id, 'request')

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
