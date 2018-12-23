from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from app.lib.rss.arxiv import ArxivRss
from app.models import RssFetchSubject


@require_POST
@csrf_exempt
@transaction.atomic
def api_jobs_fetchrss(request):
    paper_count = 0
    for subject in RssFetchSubject.objects.all():
        arxiv_rss = ArxivRss(subject)
        papers = arxiv_rss.fetch_and_save()
        paper_count += len(papers)

    return JsonResponse({
        'message': f'Successfully fetch and save {paper_count} papers from RSS.',
    })
