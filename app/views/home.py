from django.shortcuts import render
from app.models import RssFetchSubject, Paper


def home(request):
    subjects = RssFetchSubject.objects.all()
    subjects_jsonable = {subject.id: subject.dumps() for subject in subjects}

    papers = Paper.objects.order_by('-id').all()[:100]\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')

    papers_jsonable = []
    for paper in papers:
        paper_dict = paper.dumps()
        paper_dict['rss_fetch_subject_id'] = paper.rss_fetch_history.rss_fetch_subject_id
        papers_jsonable.append(paper_dict)

    return render(request, 'home.html', {
        'subjects': subjects_jsonable,
        'papers': papers_jsonable,
    })
