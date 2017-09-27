from django.shortcuts import render
from app.views.helpers import (
    create_jsonable_subjects,
    create_jsonable_papers,
)


def home(request):
    jsonable_subjects = create_jsonable_subjects()
    jsonable_papers = create_jsonable_papers()

    return render(request, 'home.html', {
        'subjects': jsonable_subjects,
        'papers': jsonable_papers,
    })
