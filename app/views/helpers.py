from datetime import datetime, timedelta

import pytz

from app.models import Paper, RssFetchSubject

TIMEZONE = pytz.timezone('Asia/Tokyo')


def create_jsonable_subjects():
    subjects = RssFetchSubject.objects.all()
    return [subject.dumps() for subject in subjects]


def create_jsonable_submit_types():
    jsonable_submit_types = []

    for submit_type, submit_type_title in Paper.SUBMIT_TYPES:
        jsonable_submit_types.append({
            'name': submit_type,
            'display_name': submit_type_title,
        })

    return jsonable_submit_types


def _split_query(query):
    query_elements = query.replace('　', ' ').split(' ')
    query_elements_en = [q for q in query_elements if q.encode('utf-8').isalnum()]
    query_elements_ja = [q for q in query_elements if q not in query_elements_en]

    return query_elements_en, query_elements_ja


def filter_papers_with_query(papers, query):
    if not query:
        return papers

    query_elements_en, query_elements_ja = _split_query(query)

    if query_elements_en:
        for query_element in query_elements_en:
            query_element_lower = query_element.lower()
            papers = [p for p in papers if query_element_lower in p.title.lower()]
    if query_elements_ja:
        for query_element in query_elements_ja:
            papers = [p for p in papers if query_element in p.title_ja]

    return papers


def format_jsonable_date_to_papers(papers):
    jsonable_fetch_date_to_papers = {}

    for paper in papers:
        paper_dump = paper.dumps()
        paper_dump['rss_fetch_subject_id'] = paper.rss_fetch_history.rss_fetch_subject_id
        fetch_date = paper.get_fetch_date(TIMEZONE)
        jsonable_fetch_date_to_papers.setdefault(fetch_date, []).insert(0, paper_dump)

    return jsonable_fetch_date_to_papers


def fetch_papers_with_offset(offset=0):
    limit = 100

    return Paper.objects.order_by('-id').all()[offset:offset+limit]\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')


def _get_search_datetime_as_range(date):
    request_dt = datetime.strptime(date, '%Y-%m-%d')
    request_dt = TIMEZONE.localize(request_dt)
    end_dt = request_dt.replace(hour=21)
    start_dt = end_dt - timedelta(days=1)

    return start_dt, end_dt


def fetch_papers_with_date(date):
    start_dt, end_dt = _get_search_datetime_as_range(date)

    return Paper.objects.order_by('-id').filter(created_at__range=(start_dt, end_dt)).all()\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')


def fetch_papers_with_query(query):
    limit = 1000

    query_elements_en, query_elements_ja = _split_query(query)

    query_set = Paper.objects

    if query_elements_en:
        for query_element in query_elements_en:
            query_set = query_set.filter(title__icontains=query_element)
    if query_elements_ja:
        for query_element in query_elements_ja:
            query_set = query_set.filter(title_ja__icontains=query_element)

    return query_set.order_by('-id').all()[:limit]\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')
