from django.shortcuts import render
from app.views.helpers import (
    create_jsonable_subjects,
    create_jsonable_date_to_papers,
    create_jsonable_submit_types,
)


def home(request):
    jsonable_subjects = create_jsonable_subjects()
    jsonable_date_to_papers = create_jsonable_date_to_papers()
    jsonable_submit_types = create_jsonable_submit_types()

    return render(request, 'home.html', {
        'subjects': jsonable_subjects,
        'date_to_papers': jsonable_date_to_papers,
        'submit_types': jsonable_submit_types,
    })
