from app.models import RssFetchSubject, Paper


def create_jsonable_subjects():
    subjects = RssFetchSubject.objects.all()
    return [subject.dumps() for subject in subjects]


def create_jsonable_date_to_papers(offset=0):
    limit = 100

    papers = Paper.objects.order_by('-id').all()[offset:offset+limit]\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')

    jsonable_fetch_date_to_papers = {}
    for paper in papers:
        paper_dump = paper.dumps()
        paper_dump['rss_fetch_subject_id'] = paper.rss_fetch_history.rss_fetch_subject_id
        fetch_datetime = paper.rss_fetch_history.get_fetch_datetime()
        jsonable_fetch_date_to_papers.setdefault(fetch_datetime.date().isoformat(), []).append(paper_dump)

    return jsonable_fetch_date_to_papers


def create_jsonable_submit_types():
    jsonable_submit_types = []

    for submit_type, submit_type_title in Paper.SUBMIT_TYPES:
        jsonable_submit_types.append({
            'name': submit_type,
            'display_name': submit_type_title,
        })

    return jsonable_submit_types
