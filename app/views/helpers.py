from datetime import datetime, timedelta
import pytz
from app.models import RssFetchSubject, Paper

TIMEZONE = pytz.timezone('Asia/Tokyo')


def create_jsonable_subjects():
    subjects = RssFetchSubject.objects.all()
    return [subject.dumps() for subject in subjects]


def _format_jsonable_date_to_papers(papers):
    jsonable_fetch_date_to_papers = {}

    for paper in papers:
        paper_dump = paper.dumps()
        paper_dump['rss_fetch_subject_id'] = paper.rss_fetch_history.rss_fetch_subject_id
        fetch_date = paper.get_fetch_date(TIMEZONE)
        jsonable_fetch_date_to_papers.setdefault(fetch_date, []).insert(0, paper_dump)

    return jsonable_fetch_date_to_papers


def create_jsonable_date_to_papers_with_offset(offset=0):
    limit = 100

    papers = Paper.objects.order_by('-id').all()[offset:offset+limit]\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')

    return _format_jsonable_date_to_papers(papers)


def _get_search_datetime_as_range(date):
    request_dt = datetime.strptime(date, '%Y-%m-%d')
    request_dt = TIMEZONE.localize(request_dt)
    end_dt = request_dt.replace(hour=21)
    start_dt = end_dt - timedelta(days=1)

    return start_dt, end_dt


def create_jsonable_date_to_papers_with_date(date):
    start_dt, end_dt = _get_search_datetime_as_range(date)

    papers = Paper.objects.order_by('-id').filter(created_at__range=(start_dt, end_dt)).all()\
        .prefetch_related('rss_fetch_history')\
        .prefetch_related('authors')

    return _format_jsonable_date_to_papers(papers)


def create_jsonable_submit_types():
    jsonable_submit_types = []

    for submit_type, submit_type_title in Paper.SUBMIT_TYPES:
        jsonable_submit_types.append({
            'name': submit_type,
            'display_name': submit_type_title,
        })

    return jsonable_submit_types
